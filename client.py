import sys
from socketio import Client
from socketio.exceptions import ConnectionError
from threading import Timer

# https://www.section.io/engineering-education/how-to-perform-threading-timer-in-python/
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)

def print_working():
    print ("still working...")

try:
    n = int(sys.argv[1])
except:
    print('please provide an integer!')
    quit()

sio = Client()
try:
    sio.connect('http://localhost:5000')
except ConnectionError:
    print("can't connect to server")
    quit()

print('working...press CTRL+C or CTRL+Break to cancel')
timer = RepeatTimer(3, print_working)
sio.emit('message', n)
timer.start()

@sio.event
def connect():
    print("reconnected!")
    sio.emit('message', n)

@sio.on('response')
def response(data):
    print(data)
    timer.cancel()
    sio.disconnect()
    quit()

@sio.event
def connect_error(data):
    print("The connection to the server is lost! reconnecting...")
