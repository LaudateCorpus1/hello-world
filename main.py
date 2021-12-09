#!/usr/bin/env python3
from flask import Flask, render_template
import logging
import time
import random

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def data():
    return 'Hello world'


@app.route('/')
def route_default():
    start = time.time()
    txt = data()
    end = time.time()
    return render_template('index.html', text=txt, seconds=round(end-start, 4))


@app.route('/bad')
def route_bad():
    txt = None
    start = time.time()
    try:
        raise TypeError()
    except Exception as e:
        txt = str(e)
    end = time.time()
    return render_template('index.html', text=txt, seconds=round(end-start, 4)), 500


@app.route('/slow')
def route_slow():
    start = time.time()
    txt = data()
    time.sleep(random.randint(10, 10000)/1000)
    end = time.time()
    return render_template('index.html', text=txt, seconds=round(end-start, 4))


@app.route('/health')
def route_health():
    return 'OK'


def main(*args, **kwargs):
    logging.debug('Starting Hello-World app')


def start_flask(**kwargs):
    logging.debug('Starting web server')
    app.run(host='0.0.0.0', port=8080, debug=False)


app.before_first_request(main)

if __name__ == '__main__':
    main()
    start_flask()
