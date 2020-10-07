#select lines from aggregated_lines WHERE batch_id = (SELECT batch_id from batch WHERE created_time = (select  max(created_time) from batch) AND sport = 'NFL')


from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy
import os
from rq import Queue
from rq.job import Job 
from worker import conn

from rq_scheduler import Scheduler

import json
from flask import jsonify
import datetime
from datetime import timedelta

import pipeline

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

q = Queue(connection=conn)
#s = Scheduler(connection=conn)
from models import *
# s = Scheduler(queue=q,connection=conn)
s = Scheduler(queue=q)

def get_lines(radio):
    errors = []
    results = {}
    batch_id = datetime.datetime.utcnow().strftime("%m%d%Y%H%M%S")
    print("TIME: ",batch_id)
    try:
        batch = Batch(
            batch=batch_id,
            sport=radio
        )
        db.session.add(batch) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
        db.session.commit()
    except Exception as e:
        print("Could not enter new batch in the table", e)
    try:
        print('Running pipeline...')
        results = pipeline.run_pipeline(radio)
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
            agg = Aggregated(
                batch=batch_id,
                lines=r_string
            )
            db.session.merge(result) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
            db.session.commit()
            db.session.add(agg) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
            db.session.commit()
            return result.name
        except Exception as e:
            print(e)
            errors.append("Unable to add item to database")
            return {"error": errors}
from app import get_lines
#job = s.enqueue_in(timedelta(minutes=5),func=get_lines, args=("NFL",), repeat=None )
job = s.schedule(scheduled_time=datetime.datetime.utcnow(), func=get_lines, args=("NFL",), repeat=None, interval=300)

print('Enqueued: ', job)

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

@app.route("/getLines", methods=['POST'])
def get_lines_initial():
    #TODO: add these two lines back after the button on the FE queries this 
    data = json.loads(request.data.decode())
    print(data)
    
    radio = data['radio']
    
    queryStr = "SELECT lines from aggregated_lines WHERE batch_id = (select batch_id from batch where sport = \'" + radio + "\' order by created_time DESC LIMIT 1);"
    #print(queryStr)
    
    #result = db.engine.execute("SELECT lines from aggregated_lines WHERE batch_id = (select batch_id from batch where sport = 'NFL' order by created_time DESC LIMIT 1);")
    result = db.engine.execute(queryStr)
    r = result.first()
    #print(r[0])
    return r[0]
    

@app.route('/start', methods=["POST"])
def pull_lines():
    from app import get_lines
    data = json.loads(request.data.decode())
    radio = data['radio']
    print(radio)
    job = q.enqueue_call(func=get_lines, args=(radio,), result_ttl=5000)
    return job.get_id()

if __name__ == '__main__':
    app.run(use_reloader=False)