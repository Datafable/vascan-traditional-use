import csv
import re
import requests

class VascanSearcher:
    def __init__(self, taxon_file=None):
	self.vascan_taxon_data = self.readVascanData(taxon_file=taxon_file)

    def readVascanData(self, taxon_file=None):
	reader = csv.reader(file(taxon_file), delimiter="\t")
	header = reader.next()
	id_column = header.index("id")
	scientific_name_column = header.index("scientificName")
	genus_column = header.index("genus")
	specific_column = header.index("specificEpithet")
	rank_column = header.index("taxonRank")
	infraspecific_column = header.index("infraspecificEpithet")
	vascan_taxon_data = []
	for line in reader:
	    taxon_id = line[id_column]
	    taxon_genus = line[genus_column]
	    taxon_specific = line[specific_column]
	    taxon_rank = line[rank_column]
	    taxon_infraspecific = line[infraspecific_column]
	    vascan_taxon_data.append([taxon_id, taxon_genus, taxon_specific, taxon_rank, taxon_infraspecific])
	outfile = file("all_vascan_taxa.txt", "w+")
	for line in vascan_taxon_data:
	    outfile.write(str(line) + "\n")
	outfile.close()
	return vascan_taxon_data

    """
    _translateRank:
       input: data from dataset, parsed by GBIF name parser
       output: rank as expected in Vascan
    """
    def _translateRank(self, genus, specific, infraspecific, rank):
        if specific == None and infraspecific == None:
	    """
	    This also takes care of sp. rank
	    """
	    new_rank = "genus"
	elif rank == None and infraspecific == None:
	    new_rank = "species"
	elif rank == "subsp." and infraspecific != None:
	    new_rank = "subspecies"
	elif rank == "var." and infraspecific != None:
	    new_rank = "variety"
	else:
	    raise Exception("could not translate rank for genus: {0}, specific: {1}, infraspecific: {2}, rank: {3}".format(genus, specific, infraspecific, rank))
	return new_rank.strip()

    def SearchOnScientificName(self, genus, specific, rank, infraspecific):
        hits = []
	#print "old rank:{0}".format(rank)
	rank = self._translateRank(genus, specific, infraspecific, rank)
	#print "new rank:{0}".format(rank)
	if genus == None:
	    genus = ""
	if specific == None:
	    specific = ""
	if infraspecific == None:
	    infraspecific = ""
	if rank == None:
	    rank = ""
	for taxon in self.vascan_taxon_data:
	    taxon_id, t_genus, t_specific, t_rank, t_infraspecific = taxon
	    if t_genus.decode("latin1") == genus.decode("utf8") and t_specific.decode("latin1") == specific.decode("utf8") and t_infraspecific.decode("latin1") == infraspecific.decode("utf8") and t_rank.decode("latin1") == rank.decode("utf8"):
		hits.append(taxon)
	if hits == []:
	    print "no hits for: {0}".format(str([genus, specific, infraspecific, rank]))
	return hits
