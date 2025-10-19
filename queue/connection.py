from redis import Redis
from rq import Queue

# FIX: Changed 'valkey' to '127.0.0.1' (localhost).
# This allows the Python application running on the host machine 
# (outside Docker) to connect to the Valkey container, which is 
# exposing port 6379 on the host via the docker-compose.yml file.
queue = Queue(connection=Redis(host="127.0.0.1")) 