#!/usr/bin/python3

import sys

max_result = ("", "", -100)

def set_max(a: tuple, b: tuple):
    return a if a[2]>b[2] else b
    
for line in sys.stdin:
    line = line.strip("\n").split("|")
    line[2]= float(line[2])
    line = tuple(line)
    max_result = set_max(max_result, line)

print(max_result)