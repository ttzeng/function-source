## API for accessing my free Redis cloud service ##

This repository contains the source code of the [Cloud Function][1] which provides an API endpoint to read/write my free [Redis][3] cloud database hosted at [Redis.io][4].

Cloud Functions is a serverless execution environment for building and connecting cloud services. To support automatic management and scaling, functions must be **stateless** -- one function invocation *must not* rely on in-memory state set by a previous invocation, as invocations might be handled by different function instances, which do not share global variables, memory, file systems, or other state. To share state across function invocations, a service like [Memorystore][2] is required to persist data. In contrast to the [cost](https://cloud.google.com/memorystore/docs/redis/pricing) incurred by the MemoryStore for Redis service, `Redis.io` provides an [essential plan](https://redis.io/pricing/#essentials) that offers <30MB size of database free of change.

Instead of having cloud services access to the Redis database individually, this Cloud Function serves as an abstraction layer and an API endpoint for accessing to the Redis cloud. To commit key-value pairs to the database, pass them to the API endpoint in terms of URL parameters (also known as query strings or URL query parameters):

    $ curl https://us-west1-ttzeng-gcp.cloudfunctions.net/redis-cloud/?a=1\&b=2\&c=3

To query values of specific keys, pass only keys in the query string, the API endpoint will respond the requested key-value pairs in a JSON string:

    $ curl https://us-west1-ttzeng-gcp.cloudfunctions.net/redis-cloud/?a
    {"a": "1"}

A special value `-` is reserved to request the API endpoint deleting the associated key from the database:

    $ curl https://us-west1-ttzeng-gcp.cloudfunctions.net/redis-cloud/?b=-
    {}

Path `/dump` can be used to list all key-value pairs in the database.

    $ curl https://us-west1-ttzeng-gcp.cloudfunctions.net/redis-cloud/dump
    {"a": "1", "c": "3"}

Though `Redis.io` provides [a number of ways](https://redis.io/docs/latest/operate/rc/security/) to secure the databases, my tiny Redis database only uses the *Default user password* for data access control. Check out the `Public endpoint` and the `Default user password` of the database on the [Redis Cloud Console][5], then set up the environment variables `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD` while creating the Cloud Function.

[1]: <https://cloud.google.com/functions/> "Cloud Functions"
[2]: <https://cloud.google.com/memorystore> "Memorystore"
[3]: <https://www.ibm.com/topics/redis> "REmote DIctionary Server"
[4]: <https://redis.io/> "Redis.io"
[5]: <https://app.redislabs.com/> "Redis Cloud Console"