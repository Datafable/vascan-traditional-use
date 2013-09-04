# aggregate all lines of one record on one line
./scripts/CleanData.py data/raw/medicinal-plants.tsv data/processed/cleanedData.tsv
./scripts/OneLinePerRecord.py ./data/processed/cleanedData.tsv ./data/processed/OneLinePerRecord.csv
