#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default='5556')
parser.add_argument('-b', '--broker', default='tcp://127.0.0.1:5555')
args = parser.parse_args()