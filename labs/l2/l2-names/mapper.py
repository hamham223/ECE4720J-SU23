#!/usr/bin/env python3
import sys

for i in sys.stdin:
	parts = i.strip().split(",")
	print(parts[1]+"\t"+parts[2])

