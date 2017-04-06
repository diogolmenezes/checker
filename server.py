import datetime
from flask import Flask, render_template
from models import Checker

HOST    = 'localhost'
PORT    = 2048
REFRESH = 60
DEBUG   = True
app     = Flask(__name__)

@app.route('/')
def index():
  checker = Checker()
  results = checker.check()
  return render_template('checker.html', **dict(result=results, checker=checker, last_check=datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), refresh=REFRESH))

if __name__ == '__main__':
  app.run(host=HOST, port=PORT, debug=DEBUG)

