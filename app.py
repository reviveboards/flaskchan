from flask import Flask, render_template, request, redirect, url_for
import datetime
from util.config import load_config, random_motd
from util.logging import *
from util.db import *

app = Flask(__name__)

date = datetime.date.today()

config = load_config('config.json')

if config['logging']:
    current_log = start_logging(config['logs_path']).name
    log_config(config, current_log)
else:
    log_config(config, '')


@app.route('/')
def boards():
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM category;')

    categories = cursor.fetchall()

    cursor.execute('SELECT * FROM board;')
    list_boards = cursor.fetchall()

    cursor.close()
    connection.close()

    title = config['title']
    motd = random_motd(config)

    return render_template('boards.html',
                           categories=categories,
                           list_boards=list_boards,
                           date=date,
                           title=title,
                           motd=motd)


# @app.route('/board')
# def board():
#     return render_template('board.html',
#                            date=date)
#

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

    return render_template('board.html', date=date, this_board=this_board)


@app.route('/admin')
def admin():
    return render_template('admin.html',
                           date=date)


if __name__ == '__main__':
    app.run()
