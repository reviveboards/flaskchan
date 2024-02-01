from flask import Flask, render_template
import datetime
from util.config import load_config, random_motd

app = Flask(__name__)

date = datetime.date.today()

config = load_config('config.json')
print(f'Starting with this parameters: {config}')


@app.route('/')
def boards():
    title = config['title']
    motd = random_motd(config)

    return render_template('boards.html',
                           date=date,
                           title=title,
                           motd=motd)




if __name__ == '__main__':
    app.run()
