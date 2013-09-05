#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import re

def check_arguments():
    if len(sys.argv) != 4:
	print "usage: ./SplitMedicinalUse.py infile uses_outfile taxon_outfile"
	sys.exit(-1)
    infile, uses_outfile, taxon_outfile = sys.argv[1:]
    return [infile, uses_outfile, taxon_outfile]

def readInput(infile):
    reader = csv.reader(file(infile), delimiter="\t")
    lines = []
    header = reader.next()
    for line in reader:
	lines.append(line)
    return lines

def translate_part(part_string):
    return part_string
    """
    parts_voc = {
	"": "",
    }
    if part_string not in parts_voc.keys():
	raise Exception("Could not translate part: {0}".format(part_string))
    return parts_voc[part_string]
    """

def parseUse(use):
    if ":" in use:
	match = re.search("(^[^\[:]*?):(.*)", use)
	if match != None:
	    groups = match.groups()
	    in_part = groups[0].strip()
	    use_description = groups[1].strip()
	    try:
		part = translate_part(in_part)
	    except Exception as e:
		print "problem while translating the part {0} from the uses {1}".format(in_part, use)
		raise e
	else:
	    use_description = use
	    part = ""
    else:
	use_description = use
	part = ""
    return [part, use_description]

def splitUsesFromLines(inlines):
    outlines = []
    for line in inlines:
	uses = line[-1]
	inline_id = line[0]
	vascan_taxon_id = line[1]
	uses_list = uses.split("|")
	for use in uses_list:
	    if use != "":
		part, use_description = parseUse(use)
		typ = "traditional medicinal use"
		source = "http://doi.org/10.1186/1746-4269-8-7"
		outline = [inline_id, use_description, typ, source, part]
		outlines.append(outline)
    return outlines

def removeUsesFromLines(inlines):
    outlines = []
    for line in inlines:
	id, taxon_concept, match_type, scientific_name, family, synonym, habit, medicinal_use = line
	outlines.append([id, taxon_concept, scientific_name, family, habit])
    return outlines

def writeTaxonOutput(taxon_outfile, outlines):
    out = file(taxon_outfile, "w+")
    header = ["id", "taxonConceptID", "scientificName", "family", "_habit"]
    outlines.insert(0, header)
    for line in outlines:
	out.write("\t".join(line) + "\n")
    out.close()

def writeUsesOutput(uses_outfile, outlines):
    out = file(uses_outfile, "w+")
    header = ["id", "description", "type", "source", "_plantPart"]
    outlines.insert(0, header)
    for line in outlines:
	out.write("\t".join(line) + "\n")
    out.close()

def main():
    infile, uses_outfile, taxon_outfile = check_arguments()
    inlines = readInput(infile)
    uses_outlines = splitUsesFromLines(inlines)
    taxon_outlines = removeUsesFromLines(inlines)
    writeTaxonOutput(taxon_outfile, taxon_outlines)
    writeUsesOutput(uses_outfile, uses_outlines)

main()
