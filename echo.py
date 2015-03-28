#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop, zmqstream

def echo(stream, message):
    stream.send_multipart(message)

io_loop = ioloop.IOLoop()
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(socket, io_loop=io_loop)
stream.on_recv_stream(echo)
socket.bind('tcp://0.0.0.0:11235')
io_loop.start()