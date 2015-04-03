#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import shlex

def fail (message) :
	print "failed=True msg=\""+message+"\""
	sys.exit (1)

def _parse (fname) :
	try :
		args_data = file (fname).read()
	except OSError as e :
		fail ("unable to open arguments file '"+fname+"'")
	arguments = shlex.split(args_data)
	args = {}
	for arg in arguments :
		if '=' in arg :
			(key, value) = arg.split('=')
			args[key] = value
	return args

def parse () :
	if len(sys.argv) != 2 :
		fail ("expecting 1 argument")
	filename = sys.argv[1]
	return _parse (filename)

if __name__=="__main__" :
	arguments = _parse ('ansible_args.txt')
	print arguments
	sys.argv+=('ansible_args.txt',)
	arguments = parse()
	print arguments
