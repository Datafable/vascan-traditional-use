#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import re

def check_arguments():
    if len(sys.argv) != 4:
	print "usage: ./SplitVernecularNames.py infile names_outfile taxon_outfile"
	sys.exit(-1)
    infile, names_outfile, taxon_outfile = sys.argv[1:]
    return [infile, names_outfile, taxon_outfile]

def readInput(infile):
    reader = csv.reader(file(infile), delimiter="\t")
    lines = []
    header = reader.next()
    for line in reader:
	lines.append(line)
    return lines

def translate_language(lang_string):
    language_voc = {
	"": "",
	"Abenaki": "Abenaki",
	"Algonquian": "Algonquian",
	"Algonquin": "Algonquin",
	"Atikamekw": "Atikamekw",
	"Chipewyan": "Chipewyan",
	"Chippewa": "Chippewa",
	"Cree": "Cree",
	"Dene": "Dene",
	"Eng.": "English",
	"Fr.": "French",
	"Innu": "Innu",
	"Innu/Montagnais": "Montagnais/Innu",
	"Malecite": "Malecite",
	"Mi'kmaq": "Mi'kmaq",
	"Montagnais": "Montagnais",
	"Montagnais/Innu": "Montagnais/Innu",
	"Ojibwa": "Ojibwa",
    }
    if lang_string not in language_voc.keys():
	raise Exception("Could not translate language: {0}".format(lang_string))
    return language_voc[lang_string]

def splitNamesFromLines(inlines):
    outlines = []
    for line in inlines:
	vernacular_names = line[7]
	inline_id = line[0]
	vascan_taxon_id = line[1]
	names_list = vernacular_names.split(";")
	for name in names_list:
	    if name != "":
		match = re.search("(.*)\((.*)\)", name)
		if match != None:
		    groups = match.groups()
		    v_names = groups[0].strip()
		    in_language = groups[1].strip()
		    try:
			language = translate_language(in_language)
		    except Exception as e:
			print "problem while translating the language {0} from the names {1}".format(in_language, name)
			raise e
		    for v_name in v_names.split(","):
			outline = [inline_id, vascan_taxon_id, language, v_name.strip()]
			outlines.append(outline)
		else:
		    raise Exception("Could not parse name: {0}".format(name))
    return outlines

def removeVNamesFromLines(inlines):
    outlines = []
    for line in inlines:
	line.pop(7)
	outlines.append(line)
    return outlines

def writeTaxonOutput(taxon_outfile, outlines):
    out = file(taxon_outfile, "w+")
    header = ["id", "_vascanTaxonID", "_taxonMatchType", "scientificName", "family", "_synonym", "_habit", "_rawMedicinalUses"]
    outlines.insert(0, header)
    for line in outlines:
	out.write("\t".join(line) + "\n")
    out.close()

def writeNamesOutput(names_outfile, outlines):
    out = file(names_outfile, "w+")
    header = ["id", "_vascanTaxonID", "_languageName", "vernacularName"]
    outlines.insert(0, header)
    for line in outlines:
	out.write("\t".join(line) + "\n")
    out.close()

def main():
    infile, names_outfile, taxon_outfile = check_arguments()
    inlines = readInput(infile)
    names_outlines = splitNamesFromLines(inlines)
    taxon_outlines = removeVNamesFromLines(inlines)
    writeTaxonOutput(taxon_outfile, taxon_outlines)
    writeNamesOutput(names_outfile, names_outlines)

main()
