#!/usr/bin/env python2.7

import argparse
import sys
from readset import *
import pipeline

# import config... this should create the global variable for use
from config import *

# argparse help description
parser = argparse.ArgumentParser(description="Create a CWL DNASeq Workflow")
# parse the name of the folder to create
parser.add_argument("name", action="store")
# parser.add_argument("-s", action="store", dest="s",
# 	help="the steps to run")

# parsing for the config file
parser.add_argument("-c", action="store", dest="config_file",
	help="specify the config file to use")
# parsing for the readset file
parser.add_argument("-readset", action="store", dest="readset",
	help="specify the readset file to use")
# setting the args to check for
args = parser.parse_args(sys.argv[1:])

try:
	config_file = open(args.config_file)
	r = config_file.readline()
	config.parse_files([config_file])
except:
	if args.config_file:
		print "can't open config_file at: "	+ args.config_file


dnaseq = pipeline.DNASeq(args.name)
dnaseq.readset += parse_illumina_readset_file(args.readset)
dnaseq.build()

