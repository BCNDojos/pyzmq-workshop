#!/usr/bin/env python
import zmq

context = zmq.Context()

s = context.socket(zmq.DEALER)
s.connect('tcp://127.0.0.1:11235')
for i in range(10):
    s.send('Hello world')
    print(s.recv())