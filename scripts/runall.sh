echo "usage: ./scripts/runall.sh /full/path/to/vascan/taxon.txt"
# aggregate all lines of one record on one line
./scripts/CleanData.py data/raw/medicinal-plants.tsv data/processed/cleanedData.tsv

# clean some data
./scripts/OneLinePerRecord.py ./data/processed/cleanedData.tsv ./data/processed/OneLinePerRecord.tsv

# cross map with vascan; the $1 will be filled in by your command line argument and should point to the vascan taxon.txt file
./scripts/MapToVascan.py ./data/processed/OneLinePerRecord.tsv $1 ./data/processed/Mapped.tsv

# split vernacular names
./scripts/SplitVernacularNames.py data/processed/Mapped.tsv data/dwc-a/vernacularname.tsv data/processed/taxon_names_split.tsv

# split medicinal uses
./scripts/SplitMedicinalUse.py ./data/processed/taxon_names_split.tsv ./data/dwc-a/medicinaluse.tsv ./data/dwc-a/taxon.tsv ./documentation/plant-parts-mapping.tsv 
