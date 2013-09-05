#!/usr/bin/python

import csv
import sys

def check_arguments():
    if len(sys.argv) != 3:
	print "usage: ./OneLinePerRecord.py infile outfile"
	sys.exit(-1)
    infile, outfile = sys.argv[1:]
    return [infile, outfile]

def createRecord(scientific_name, family_and_habit, vernacular_names, medicinal_uses):
    if "," in family_and_habit:
	family, growth_habit = family_and_habit.split(",")
    else:
	family = family_and_habit
	growth_habit = ""
    p_references = "|".join(medicinal_uses)
    record = [scientific_name, family.strip(), growth_habit.strip(), vernacular_names, p_references]
    return record

def create_record_from_record_lines(record_lines):
    scientific_name, vernacular_names, medicinal_uses1 = record_lines.pop(0)
    family_and_habit, empty_field, medicinal_uses2 = record_lines.pop(0)
    medicinal_uses = [medicinal_uses1, medicinal_uses2]
    if len(record_lines) > 2:
	    for remaining_line in record_lines:
	        empty_field1, empty_field2, references3 = remaining_line
	        medicinal_uses.append(references3)
    record = createRecord(scientific_name, family_and_habit, vernacular_names, medicinal_uses)
    return record

def sortLinesPerRecord(reader):
    lines_per_record = []
    record_lines = []
    for entry_line in reader:
	if entry_line == []:
	    pass;# skip empty lines
	else:
	    if entry_line[1] != "":
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
    out_header = ["scientificName", "family or synonym", "habit", "rawVernacularNames", "rawMedicinalUses"]
    records.append(out_header)
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
