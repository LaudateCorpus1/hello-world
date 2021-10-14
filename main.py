#!/usr/bin/env python3
from flask import Flask, render_template
import peewee
import os
import json
import logging
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
import opencensus.trace.tracer
import time
import random
import math

logging.basicConfig(level=logging.DEBUG)

db_host = os.environ.get("DB_HOST", "localhost")
db_user = os.environ.get("DB_USER", "postgres")
db_password = os.environ.get("DB_PASSWORD", "1234")
db_name = os.environ.get("DB_NAME", "hello-world-db")

app = Flask(__name__)
db = peewee.PostgresqlDatabase(db_name, host=db_host, user=db_user, password=db_password)


@app.route('/')
def route_default():
    start = time.time()
    data = Text.get_by_id(1)
    end = time.time()
    return render_template('index.html', text=data.text, seconds=round(end-start, 4))


@app.route('/bad')
def route_bad():
    start = time.time()
    try:
        Text.get_by_id(100)
    except Exception as e:
        data = str(e)
    end = time.time()
    return render_template('index.html', text=data, seconds=round(end-start, 4)), 500


@app.route('/slow')
def route_slow():
    start = time.time()
    data = Text.get_by_id(1)
    time.sleep(random.randint(10, 10000)/1000)
    end = time.time()
    return render_template('index.html', text=data.text, seconds=round(end-start, 4))


@app.route('/health')
def route_health():
    return 'OK'


class Text(peewee.Model):
    text = peewee.TextField()

    class Meta:
        database = db


def init_tracer():
    if os.environ.get("DISABLE_TRACING", None):
        return
    logging.debug("Initializing OpenCensus tracer")
    exporter = stackdriver_exporter.StackdriverExporter(
        project_id='idme-328822',
    )
    tracer = opencensus.trace.tracer.Tracer(
        exporter=exporter,
        sampler=opencensus.trace.tracer.samplers.AlwaysOnSampler()
    )
    return tracer


def init_database():
    logging.debug('Applying models to database')
    db.create_tables([Text])
    exists = Text.get_or_none(Text.id == 1)
    if not exists:
        logging.debug('Database is empty; adding data to tables')
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        res = Text(text=data['text'])
        res.save(force_insert=True)


def main(*args, **kwargs):
    logging.debug('Starting Hello-World app')
    init_tracer()
    init_database()


def start_flask(**kwargs):
    logging.debug('Starting web server')
    app.run(host='0.0.0.0', port=8080, debug=False)


app.before_first_request(main)

if __name__ == '__main__':
    main()
    start_flask()
