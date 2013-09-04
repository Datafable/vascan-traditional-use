#!/usr/bin/python

import sys

infile_name = sys.argv[1]
outfile_name = sys.argv[2]

infile = file(infile_name)
outfile = file(outfile_name, "w+")

# write header
outfile.write(infile.next())
for line in infile:
    cleaned_line = line
    if line[0] == "*":
	cleaned_line = line[1:]
	print "stripping '*' from line: {0}".format(line)
    outfile.write(cleaned_line)

infile.close()
outfile.close()
