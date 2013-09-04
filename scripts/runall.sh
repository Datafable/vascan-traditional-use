# aggregate all lines of one record on one line
echo "usage: ./scripts/runall.sh /full/path/to/vascan/taxon.txt"
./scripts/CleanData.py data/raw/medicinal-plants.tsv data/processed/cleanedData.tsv
./scripts/OneLinePerRecord.py ./data/processed/cleanedData.tsv ./data/processed/OneLinePerRecord.csv
./scripts/MapToVascan.py ./data/processed/OneLinePerRecord.csv $1 ./data/processed/Mapped.txt
