from flask import Flask, render_template
import datetime
from util.config import load_config, random_motd
from util.logging import *

app = Flask(__name__)

date = datetime.date.today()

config = load_config('config.json')

if config['logging']:
    current_log = start_logging(config['logs_path']).name
    log_config(config, current_log)


@app.route('/')
def boards():
    title = config['title']
    motd = random_motd(config)

    return render_template('boards.html',
                           date=date,
                           title=title,
                           motd=motd)


@app.route('/board')
def board():
    return render_template('board.html',
                           date=date)


@app.route('/admin')
def admin():
    return render_template('admin.html',
                           date=date)


if __name__ == '__main__':
    app.run()
