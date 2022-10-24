
import sys
from flask import Flask
from flask_socketio import SocketIO, emit

from redis import Redis
from rq import Queue

sys.set_int_max_str_digits(10000000)

r = Redis('myredis', 6379)
q = Queue(connection=r)

app = Flask(__name__)
socketio = SocketIO(app, transport='websocket')

@socketio.on('message')
def message(n):
    job = q.enqueue('fibo.fib', n, job_id=str(n), result_ttl=86400)
    while job.result == None:
        job.refresh()
    emit('response', str(job.result))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
