#!/usr/bin/env python
import argparse
import random
import zmq

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--broker', default='tcp://127.0.0.1:5555')

cities = open('cities.txt').readlines()

def get_hiders():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.DEALER)
    zmq_socket.connect(args.broker)
    zmq_socket.send('LIST')
    return zmq_socket.recv().split()

def choose_city():
    return random.choice(cities).strip()

def guess(hider):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.DEALER)
    print 'tcp://{}'.format(hider.strip())
    zmq_socket.connect('tcp://{}'.format(hider.strip()))
    city = choose_city()
    print 'SEEKER: Chosen', city
    zmq_socket.send(city)
    reply = zmq_socket.recv()
    if reply == 'CORRECT':
        print 'SEEKER: Found {} in {}'.format(hider, city)

if __name__ == '__main__':
    args = parser.parse_args()
    hiders = get_hiders()
    print 'SEEKER: ', hiders
    for hider in hiders:
        guess(hider)
