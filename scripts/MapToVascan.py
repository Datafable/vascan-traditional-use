#!/usr/bin/python

import sys
import os
import csv
import requests
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir + "/scripts/")
import DwCReader as vs

def check_arguments():
    if len(sys.argv) != 4:
	print "usage: ./MapToVascan.py infile vascan_taxon_file outfile"
	sys.exit(-1)
    infile, vascan_taxon_file, outfile = sys.argv[1:]
    return [infile, vascan_taxon_file, outfile]

def replace_spaces_and_ampersands_for_request(in_names):
    out_names = []
    for name in in_names:
	out_name1 = name.replace(" ", "%20")
	out_name2 = out_name1.replace("&", "and")
	out_names.append(out_name2)
    return out_names

def getJsonNameParts(names):
    max_names_in_request = 200
    j = 0
    chunks = [names[i:i+max_names_in_request] for i in range(0, len(names), max_names_in_request)]
    json_data_list = []
    for chunk_of_names in chunks:
	r = requests.post("http://ecat-dev.gbif.org/ws/parser?names={0}".format("|".join(chunk_of_names)))
	json_data_list += r.json()["data"]
    return json_data_list

def parseAllNames(scientific_names):
    names = replace_spaces_and_ampersands_for_request(scientific_names)
    json_data = getJsonNameParts(names)
    print "number of names sent to GBIF: {0}".format(len(names))
    print "number of names got from GBIF: {0}".format(len(json_data))
    output = [{"genus": x["genus"], "specific": x["specific"], "rank": x["rank"], "infraspecific": x["infraSpecific"]} for x in json_data]
    return output

def getNames(lines):
    names = []
    for line in lines:
	scientific_name = line[0]
	names.append(scientific_name)
    name_components = parseAllNames(names)
    return name_components

def map_names_on_vascan(names, incsv_lines, taxonfile):
    searcher = vs.VascanSearcher(taxon_file=taxonfile)
    mapped_hits = []
    for i in range(len(names)):
	name_components = names[i]
	incsv_line = incsv_lines[i]
	print "mapping {0}".format(name_components)
	hits = searcher.SearchOnScientificName(name_components["genus"], name_components["specific"], name_components["rank"], name_components["infraspecific"])
	if len(hits) == 1:
	    incsv_line.insert(0, "single")
	    incsv_line.insert(0, "http://data.canadensys.net/vascan/taxon/" + hits[0][0])
	    mapped_hits.append(incsv_line)
	elif len(hits) == 0:
	    incsv_line.insert(0, "none")
	    incsv_line.insert(0, "")
	    mapped_hits.append(incsv_line)
	else:
	    incsv_line.insert(0, "several")
	    incsv_line.insert(0, "")
	    mapped_hits.append(incsv_line)
    return mapped_hits

def printReport(one_found, several_found, none_found):
    print "Nr of entries that returned one vascan hit: {0}".format(len(one_found))
    print "Nr of entries that returned several vascan hits: {0}".format(len(several_found))
    print "Nr of entries that returned no vascan hits: {0}".format(len(none_found))
    print "thos that match several times: \n{0}".format(str(several_found))
    print "those that don't match: \n{0}".format(str(none_found))

def write_output(outlines, outfile):
    out = file(outfile, "w+")
    header = ["id", "vascan_taxon_id", "taxon_match_type", "scientificName", "family", "synonym", "habit", "rawVernacularNames", "rawMedicinalUses"]
    out.write("\t".join(header) + "\n")
    id = 1
    for line in outlines:
	line.insert(0, str(id))
	out.write("\t".join(line) + "\n")
	id += 1
    out.close()

def getCsvLines(infile):
    infile_reader = csv.reader(file(infile), delimiter="\t")
    header = infile_reader.next()
    lines = []
    for line in infile_reader:
	lines.append(line)
    return lines

def main():
    infile, vascan_taxon_file, outfile = check_arguments()
    incsv_lines = getCsvLines(infile)
    names = getNames(incsv_lines)
    mapped_hits = map_names_on_vascan(names, incsv_lines, vascan_taxon_file)
    #printReport(mapped_hits)
    write_output(mapped_hits, outfile)

main()
