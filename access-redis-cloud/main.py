import os

import json
import functions_framework
import redis

# Leave the connection pool global to prevent hitting the connection limit
redis_pool = redis.ConnectionPool(host=os.environ['REDIS_HOST'],
                                  port=os.environ['REDIS_PORT'],
                                  password=os.environ['REDIS_PASSWORD'])

@functions_framework.http
def access_redis_cloud(request):
    r = redis.Redis(connection_pool=redis_pool)

    queries = {}
    if request.path == '/dump':
        # Dump the entire database
        for k in r.keys():
            # Both keys and values got from Redis are bytes, must convert to strings
            queries[k.decode('utf-8')] = r.get(k).decode('utf-8')
        return json.dumps(queries)

    try:
        # Iterate (k,v) pairs in the query string embedded in the URL
        for k in request.args:
            v = request.args.get(k)
            if not v:
                # Query Redis cloud on key's value if caller didn't specify
                v = r.get(k)
                if v is not None:
                    queries[k] = v.decode('utf-8')
            else:
                # Commit / delete the key value pair to / from Redis cloud
                if v == '-':
                    r.delete(k)
                else:
                    r.set(k, v)
    except Exception as e:
        print('Redis connection error: ', e)
    return json.dumps(queries)
