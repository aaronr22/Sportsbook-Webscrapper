#Needed for the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 
import datetime

import sys

#Needed for the pipeline
import pipeline
import json
from models import *

#Needed for redis
from rq import Queue
from rq.job import Job 
from worker import conn

#Needed for the scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

#connect to db
engine = create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(bind=engine)
session = Session()

q = Queue(connection=conn)

#aggregate lines and push to db
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
        session.add(batch) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
        session.commit()
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
            session.merge(result) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
            session.commit()
            session.add(agg) #CHANGE TO ADD IF WE ARE DOING A NEW INSERT EACH TIME
            session.commit()
            return result.name
        except Exception as e:
            print(e)
            errors.append("Unable to add item to database")
            return {"error": errors}

#get_lines("CFB")
# result = db.execute("SELECT * from aggregated_lines")
# for r in result:
#     print(r)
def redis_test(v):
    d = datetime.datetime.utcnow().strftime("%m%d%Y%H%M%S")
    print("I am testing redis: ", v, d)
    return "Success"

#@sched.scheduled_job('interval', minutes=2)

def timed_job():
    print(3)
    from app import get_lines
    print('Scheduling...')
    job = q.enqueue_call(func=get_lines, args=("CFB",))
    job2 = q.enqueue_call(func=get_lines, args=("NFL",))
    print(job.get_id(), job2.get_id)

print(1)
sched.add_job(timed_job)
sched.add_job(timed_job, 'interval', minutes=10)
print(2)
sched.start()
#from app import redis_test
# if __name__ == '__main__':
#     from clock import get_lines
#     job = q.enqueue_call(func=get_lines, args=("CFB",), result_ttl=5000)
#     print(job.get_id())