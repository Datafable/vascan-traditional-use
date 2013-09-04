#!/usr/bin/python

import csv
import sys

def check_arguments():
    if len(sys.argv) != 3:
	print "usage: ./RawDataReader.py infile outfile"
	sys.exit(-1)
    infile, outfile = sys.argv[1:]
    return [infile, outfile]

def createRecord(l_name, bf_and_ghabit, v_names, parts_references):
    if "," in bf_and_ghabit:
	family, growth_habit = bf_and_ghabit.split(",")
    else:
	family = bf_and_ghabit
	growth_habit = ""
    p_references = "|".join(parts_references)
    record = [l_name, family.strip(), growth_habit.strip(), v_names, p_references]
    return record

def create_record_from_record_lines(record_lines):
    latin_name, vernacular_names, parts_references1 = record_lines[0]
    botanical_family_and_growth_habit, empty_field, parts_references2 = record_lines[1]
    parts_references = [parts_references1, parts_references2]
    if len(record_lines) > 2:
	for remaining_line in record_lines:
	    empty_field1, empty_field2, references3 = remaining_line
	    parts_references.append(references3)
    record = createRecord(latin_name, botanical_family_and_growth_habit, vernacular_names, parts_references)
    return record

def sortLinesPerRecord(reader):
    lines_per_record = []
    record_lines = []
    for entry_line in reader:
	if entry_line == []:
	    pass;# skip empty lines
	else:
	    if entry_line[0] != "" and entry_line[1] != "":
		if record_lines != []:
		    lines_per_record.append(record_lines)
		record_lines = []
	    record_lines.append(entry_line)
    lines_per_record.append(record_lines)
    return lines_per_record

def readData(infilename):
    reader = csv.reader(file(infilename), delimiter="\t")
    header = reader.next()
    records = []
    lines_per_record = sortLinesPerRecord(reader)
    for record_lines in lines_per_record:
	record = create_record_from_record_lines(record_lines)
	records.append(record)
    return records


def writeCsv(data, outfilename):
    writer = csv.writer(file(outfilename, "w+"), delimiter="\t")
    for line in data:
	writer.writerow(line)

def main():
    infile, outfile = check_arguments()
    data = readData(infile)
    writeCsv(data, outfile)

main()
