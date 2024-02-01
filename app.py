from flask import Flask, render_template
import datetime


app = Flask(__name__)

date = datetime.date.today()

title = "Flaskchan"
motd = "Reviving revivors"


@app.route('/')
def hello_world():
    return render_template('boards.html', date=date, title=title, motd=motd)


if __name__ == '__main__':
    app.run()
