#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop, zmqstream

def fibonacci(n):
    a, b = 0, 1
    while n >= a:
        yield(a)
        a, b = b, a + b
    return

def fibo(stream, message):
    n = int(message[1])
    reply = [message[0]] + [str(n in [x for x in fibonacci(n)])]
    stream.send_multipart(reply)

io_loop = ioloop.IOLoop()
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(socket, io_loop=io_loop)
stream.on_recv_stream(fibo)
socket.bind('tcp://0.0.0.0:11235')
io_loop.start()