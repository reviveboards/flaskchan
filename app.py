from flask import Flask, render_template, request, redirect, url_for
import datetime
from util.config import load_config, random_motd
from util.logging import *
from util.db import *
from util.forms import *

app = Flask(__name__)

date = datetime.date.today()

config = load_config('config.json')

version = "0.1a"

if config['logging']:
    current_log = start_logging(config['logs_path']).name
    log_config(config, current_log)
else:
    log_config(config, '')


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


def get_board_posts(board_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM post WHERE board_id = '{board_id}';")
    board_posts = cur.fetchall()

    cur.close()
    conn.close()

    return board_posts


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


def create_board(b_tag, b_cat_id, b_name, b_desc):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO board (tag, category_id, name, description) VALUES ("
                f"'{b_tag}',"
                f"'{b_cat_id}',"
                f"'{b_name}',"
                f"'{b_desc}');")
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

    title = config['title']
    motd = random_motd(config)

    return render_template('boards.html',
                           categories=categories,
                           list_boards=list_boards,
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
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM board WHERE tag = '{board_tag}';")
    this_board = cursor.fetchone()
    cursor.close()
    connection.close()

    if request.method == 'POST':
        title = request.form['postTitle']
        parent_post = 0
        parent_board = this_board[0]
        post_text = request.form['postText']
        images = [1, 1, 1]

        create_post(title, parent_post, parent_board, post_text, images, this_board[1])

    posts = get_board_posts(this_board[0])

    return render_template('board.html',
                           date=date,
                           this_board=this_board,
                           posts=posts,
                           version=version)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_categories = get_categories()

    

    return render_template('admin.html',
                           admin_categories=admin_categories,
                           date=date,
                           version=version)


if __name__ == '__main__':
    app.run()
