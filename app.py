from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy
import os
from rq import Queue
from rq.job import Job 
from worker import conn
import json
from flask import jsonify

import pipeline

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import *

def get_lines():
    errors = []
    results = {}

    try:
        print('Running pipeline...')
        results = pipeline.run_pipeline()
    except Exception as e:
        print(e)
        errors.append("Could not run pipeline")
    if bool(results):
        print('In not empty...')
        r_string = json.dumps(results)
        try:
            result = Result(
                name="data",
                lines=r_string
            )
            db.session.merge(result) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
            db.session.commit()
            return result.name
        except Exception as e:
            print(e)
            errors.append("Unable to add item to database")
            return {"error": errors}

@app.route('/test')
def hello():
    return "Hello world!"

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(name='data').first()
        return json.loads(result.lines)
        #return str(job.result), 200
    else:
        return "nay", 202


@app.route('/start', methods=["POST"])
def pull_lines():
    from app import get_lines

    job = q.enqueue_call(func=get_lines, result_ttl=5000)
    return job.get_id()

if __name__ == '__main__':
    app.run()