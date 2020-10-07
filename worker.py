import os 

import redis 
from rq import Worker, Queue, Connection 

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

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

if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work(with_scheduler=True)