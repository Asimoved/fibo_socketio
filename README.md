
# SocketIO Fibonacci Server

This simple server given integer n will calculate the nth Fibonacci number. Since this calculation can take significant time, the task is passed to a queue and ran by a worker, so it does no hang the server process. The task and the results are stored in a redis db. The components are separated into three docker containers which are orchestrated by docker compose.

Advantages:
- the services are separated, so even if the server or worker go down, existing tasks and results are kept
- the started tasks and previously calculated results are kept (for a day) so these results can be returned immediately for new queries
- if a second client asks for a calculation that has already been started, no new task will be created and the result will be provided once it is complete

## Prequisites

- git
- docker
- socketio (python-socketio for the client)

## Installation

- download or clone this repository from github: git clone https://github.com/Asimoved/fibo_socketio.git
- from the main directory run: docker compose up -d
    + docker will download the official redis image, build the app and worker images from their respective directories

## Usage

You can immediately test from the command line with: python client.py 1 (or: python3 client.py 1)

- The client will attempt to connect to the server, then send the integer and wait for the result.
- It will let you know in 3 second intervals that it's still working.
- If the connection is broken (you can simulate this by stopping the app container), the client will attempt to reconnect.
- When reconnected the client will keep waiting if the calculation is not yet complete, or return the result if it's already available.


