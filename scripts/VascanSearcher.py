import csv
import re

class VascanSearcher:
    def __init__(self, taxon_file=None):
        self.readVascanData(taxon_file=taxon_file)

    def readVascanData(self, taxon_file=None):
	reader = csv.reader(file(taxon_file), delimiter="\t")
	header = reader.next()
	self.vascan_taxon_data = []
	for line in reader:
	    taxonid, acceptedNameUsageID, parentNameUsageID, nameAccordingToID, scientificName, acceptedNameUsage, parentNameUsage, nameAccordingTo, higherClassification, taxonclass, order, family, genus, subgenus, specificEpithet, infraspecificEpithet, taxonRank, scientificNameAuthorship, taxonomicStatus, modified, bibliographicCitation, references = line

	    taxon_line = {
		"taxonid": taxonid,
		"acceptedNameUsageID": acceptedNameUsageID,
		"parentNameUsageID": parentNameUsageID,
		"nameAccordingToID": nameAccordingToID,
		"scientificName": scientificName,
		"acceptedNameUsage": acceptedNameUsage,
		"parentNameUsage": parentNameUsage,
		"nameAccordingTo": nameAccordingTo,
		"higherClassification": higherClassification,
		"taxonclass": taxonclass,
		"order": order,
		"family": family,
		"genus": genus,
		"subgenus": subgenus,
		"specificEpithet": specificEpithet,
		"infraspecificEpithet": infraspecificEpithet,
		"taxonRank": taxonRank,
		"scientificNameAuthorship": scientificNameAuthorship,
		"taxonomicStatus": taxonomicStatus,
		"modified": modified,
		"bibliographicCitation": bibliographicCitation,
		"references": references
		}
	    self.vascan_taxon_data.append(taxon_line)

    def SearchOnScientificName(self, name_string):
        hits = []
	for known_taxon in self.vascan_taxon_data:
	    match = re.search(name_string, known_taxon["scientificName"])
	    if match != None:
		hits.append(known_taxon)
	return hits
