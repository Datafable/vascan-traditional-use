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
	"Dene": "Chipewyan",
	"Eng.": "English",
	"Fr.": "French",
	"Innu": "Montagnais",
	"Innu/Montagnais": "Montagnais",
	"Malecite": "Malecite",
	"Mi'kmaq": "Mi'kmaq",
	"Montagnais": "Montagnais",
	"Montagnais/Innu": "Montagnais",
	"Ojibwa": "Ojibwe"
    }
    iso_code_voc = {
	"": "",
	"Abenaki": "ISO 639:aaq",
	"Algonquian": "ISO 639:alg",
	"Algonquin": "ISO 639:alq",
	"Atikamekw": "ISO 639:atj",
	"Chipewyan": "ISO 639:chp",
	"Chippewa": "ISO 639:ciw",
	"Cree": "ISO 639:cre",
	"Dene": "ISO 639:chp",
	"English": "ISO 639:eng",
	"French": "ISO 639:fra",
	"Innu": "ISO 639:moe",
	"Malecite": "ISO 639:pgm",
	"Mi'kmaq": "ISO 639:mic",
	"Montagnais": "ISO 639:moe",
	"Ojibwe": "ISO 639:oje"
    }

    if lang_string not in language_voc.keys():
	raise Exception("Could not translate language: {0}".format(lang_string))
    language_name = language_voc[lang_string]
    if "/" in language_name:
	l_names = language_name.split("/")
	for l_name in l_names:
	    language_iso_code = iso_code_voc[l_name]
    else:
	language_iso_code = iso_code_voc[language_name]
    return [language_name, language_iso_code]

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
			language_name, language_iso_code = translate_language(in_language)
		    except Exception as e:
			print "problem while translating the language {0} from the names {1}".format(in_language, name)
			raise e
		    for v_name in v_names.split(","):
			outline = [inline_id, v_name.strip(), "http://doi.org/10.1186/1746-4269-8-7", language_iso_code, language_name]
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
    header = ["id", "vernacularName", "source", "language", "_languageName"]
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
