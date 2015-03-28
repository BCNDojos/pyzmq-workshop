#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream

clients = set()

def action_register(message):
    address = message.split()[1].strip()
    if address in clients:
        return 'HOP'
    else:
        clients.add(address)
        return 'OK'

def action_list(message):
    return ' '.join(clients)

def handle(stream, message):
    addr, text = message
    print('BROKER: ' + text)
    action = text.split()[0].lower()
    try:
        reply = globals()['action_' + action](text)
    except KeyError:
        print('BROKER: Unknown action', action)
        reply = 'ERROR'
    stream.send_multipart((addr, reply))

io_loop = ioloop.IOLoop()
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(socket, io_loop=io_loop)
stream.on_recv_stream(handle)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

if __name__ == '__main__':
    args = parser.parse_args()
    socket.bind(args.bind_address)
    io_loop.start()