#!/usr/bin/env python
import socket
import random
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream

city = ''
cities = open('cities.txt').readlines()

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default='5556')
parser.add_argument('-b', '--broker', default='tcp://127.0.0.1:5555')

def get_ip():
    return socket.gethostbyname(socket.gethostname())

def register(port):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.DEALER)
    zmq_socket.connect(args.broker)
    zmq_socket.send('REGISTER {}:{}'.format(get_ip(), port))
    reply = zmq_socket.recv()
    if reply == 'HOP':
        port = register(str(int(port) + 1))
    zmq_socket.close()
    return port

def choose_city():
    return random.choice(cities).strip()

def handle(stream, message):
    global city
    addr, text = message
    print('HIDER: ' + text)
    if text == city:
        print('HIDER: Found!')
        reply = 'CORRECT'
        city = choose_city()
        print 'HIDER: Chosen', city
    else:
        reply = 'INCORRECT'
    stream.send_multipart((addr, reply))

io_loop = ioloop.IOLoop()
context = zmq.Context()
zmq_socket = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(zmq_socket, io_loop=io_loop)
stream.on_recv_stream(handle)

if __name__ == '__main__':
    args = parser.parse_args()
    port = register(args.port)
    print 'HIDER: Using', get_ip(), port
    city = choose_city()
    print 'HIDER: Chosen', city
    zmq_socket.bind('tcp://{}:{}'.format(get_ip(), port))
    io_loop.start()
