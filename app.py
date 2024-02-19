from flask import Flask, render_template, request, redirect, url_for

import re

from flask_wtf import CSRFProtect

from util.config import load_config, random_motd
from util.logging import *
from util.db import *
from util.forms import *

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf',
    WTF_CSRF_SECRET_KEY='v rossiyskom monitore obnaruzhili kitayskiy chip'
)

date = datetime.date.today()

csrf = CSRFProtect()

config = load_config('config.json')

version = "0.1a"

if config['logging']:
    current_log = start_logging(config['logs_path']).name
    log_config(config, current_log)
else:
    log_config(config, '')

csrf.init_app(app)


# ############ #
# Some getters #
# ############ #


def get_categories():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM category;")
    cats = cur.fetchall()

    cur.close()
    conn.close()

    return cats


def get_boards():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM board;")
    all_boards = cur.fetchall()

    cur.close()
    conn.close()

    return all_boards


def get_this_board(t):
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM board WHERE tag = '{t}';")
    this_board = cursor.fetchone()
    cursor.close()
    connection.close()

    return this_board


def get_latest_posts():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM post JOIN board ON post.board_id = board.id WHERE board.nsfw = false ORDER BY timestamp DESC LIMIT 8')
    latest_posts = cur.fetchall()
    cur.close()
    conn.close()

    return latest_posts


def get_board_posts(board_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM post WHERE board_id = '{board_id}';")
    board_posts = cur.fetchall()

    cur.close()
    conn.close()

    return board_posts


def get_op(post_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM post WHERE id = '{post_id}'")
    op = cur.fetchone()

    cur.close()
    conn.close()

    return op


def get_thread(board_tag, parent):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM post JOIN board ON post.board_id = board.id WHERE tag = '{board_tag}' AND parent_id = '{parent}';")

    p_children = cur.fetchall()

    cur.close()
    conn.close()

    return p_children


# ######## #
# Creators #
# ######## #


def create_post(post_title, parent_post, parent_board, post_text, post_images, board):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO post (title, parent_id, board_id, text, timestamp) VALUES ("
                f"'{post_title}', "
                f"'{parent_post}', "
                f"'{parent_board}', "
                f"'{post_text}', "
                f" CURRENT_TIMESTAMP);")
    conn.commit()
    cur.close()
    conn.close()

    return redirect(f"/{board}")


def create_category(cat):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO category (name) VALUES ('{cat}');")

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/admin')


def create_board(b_tag, b_cat_id, b_name, b_desc, nsfw, is_locked):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO board (tag, category_id, name, description, nsfw, is_locked) VALUES ("
                f"'{b_tag}',"
                f"'{b_cat_id}',"
                f"'{b_name}',"
                f"'{b_desc}',"
                f"{nsfw},"
                f"{is_locked});")
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/admin')


# ###### #
# Routes #
# ###### #

@app.route('/')
def boards():
    categories = get_categories()

    list_boards = get_boards()

    p_latest = get_latest_posts()

    title = config['title']
    motd = random_motd(config)

    return render_template('boards.html',
                           categories=categories,
                           list_boards=list_boards,
                           p_latest=p_latest,
                           date=date,
                           title=title,
                           motd=motd,
                           version=version)


# @app.route('/board')
# def board():
#     return render_template('board.html',
#                            date=date)
#


@app.route('/<string:board_tag>', methods=['GET', 'POST'])
def get_board(board_tag):
    tb = get_this_board(board_tag)

    n_p_form = NewPostForm()

    if n_p_form.validate_on_submit():
        p_title = n_p_form.post_title.data
        parent_board = tb[0]
        p_text = n_p_form.post_text.data

        reply_pattern = r'^(?:>>)(\d+)'
        parent_post = re.search(reply_pattern, p_text)
        images = [1, 1, 1]

        create_post(p_title, parent_post[1], parent_board, p_text, images, tb[1])

    posts = get_board_posts(tb[0])

    return render_template('board.html',
                           date=date,
                           this_board=tb,
                           n_p_form=n_p_form,
                           posts=posts,
                           version=version)


@app.route('/<string:board_tag>/<int:op_id>', methods=['GET', 'POST'])
def thread(board_tag, op_id):
    n_p_form = NewPostForm()

    op = get_op(op_id)
    replies = get_thread(board_tag, op[0])

    return render_template('thread.html',
                           op=op,
                           replies=replies,
                           n_p_form=n_p_form,
                           date=date,
                           version=version)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_categories = get_categories()

    n_b_form = NewBoardForm()
    n_c_form = NewCategoryForm()

    n_b_form.board_category.choices = [(cat[0], cat[1]) for cat in admin_categories]

    if n_b_form.validate_on_submit():
        b_name = n_b_form.board_name.data
        b_desc = n_b_form.board_description.data
        b_tag = n_b_form.board_tag.data
        b_cat_id = n_b_form.board_category.data
        is_nsfw = n_b_form.is_nsfw.data
        is_locked = n_b_form.is_locked.data

        create_board(b_tag, b_cat_id, b_name, b_desc, is_nsfw, is_locked)
    elif n_c_form.validate_on_submit():
        c_name = n_c_form.category_name.data

        create_category(c_name)

    return render_template('admin.html',
                           admin_categories=admin_categories,
                           date=date,
                           version=version,
                           n_b_form=n_b_form,
                           n_c_form=n_c_form)


if __name__ == '__main__':
    app.run()
