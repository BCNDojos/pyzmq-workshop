#!/usr/bin/env python
import zmq
from random import randint

context = zmq.Context()

s = context.socket(zmq.DEALER)
s.connect('tcp://127.0.0.1:11235')
for i in range(15):
    n = randint(0,200)
    s.send(str(n))
    print(str(n) + ' ' + s.recv())