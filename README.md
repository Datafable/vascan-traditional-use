# Traditional use of medicinal plants in Canada

## Rationale

The paper:

> Uprety Y, Asselin H, Dhakal A, Julien N. 2012. Traditional use of medicinal plants in the boreal forests of Canada: review and perspectives. J Ethnobiol Ethnomed. 2012;9:7. doi: [10.1186/1746-4269-8-7](http://doi.org/10.1186/1746-4269-8-7).

... contains a [fantastic dataset](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3316145/#__sec25title) in the supplementary data about the traditional medicinal use and vernacular names of plants in Canada. The paper (and thus supplementary data) are published under [Creative Commons Attribution](http://creativecommons.org/licenses/by/2.0). The data however are provided as a **Word file** and thus not readily usable.

## Challenge

During the 4-day course of the [#BIH13 conference](http://conference.lifewatch.unisalento.it/index.php/EBIC/BIH2013), we will attempt to transform the data to a usable CSV file and link the data up with the [Database of Vascular Plants of Canada (VASCAN)](http://data.canadensys.net/vascan/), in which @peterdesmet is [involved](https://github.com/peterdesmet/vascan-data-paper).

## Result

We managed to translate the dataset into a Darwin Core Archive, within the timeframe of the conference. See "Steps" below for the full details.

* [Structure of the archive](data/dwc-a)
* [Download the archive](data/dwc-a.zip)

## Steps

1. Copy/paste the [Word table](data/raw/medicinal-plants.doc) to a [CSV file](data/raw/medicinal-plants.tsv).
2. Get the data for one record (a taxon) on one line. [[script](scripts/OneLinePerRecord.py)]
3. Fix some formatting (mostly manually). [[script](scripts/CleanData.py)]
4. Run the `scientificName` through the [GBIF name parser](http://tools.gbif.org/nameparser/) and try to match the returned `genus`, `specificEpithet`, `infraspecificEpithet` and `taxonRank` with data from [VASCAN](http://dx.doi.org/10.5886/1bft7W5f). [[script](scripts/MapToVascan.py)]

   Of the `545` names, `493` had one exact match, `48` no match, and `4` several matches. We tried to explain the mismatches [here](documentation/mismatch-remarks.tsv).
5. Realize that there are too many vernacular name languages ([14](documentation/language-mapping.tsv)) and especially used plant parts ([129](documentation/plant-parts-mapping.tsv)) to express this in a flat file. Express as a Darwin Core Archive instead. [[target format file](documentation/target-format.md)]
6. Express the `scientificName`, `family` and mapping to VASCAN in a [Taxon Core](http://rs.gbif.org/core/dwc_taxon.xml). We also included the non-DwC term `_habit`.
6. Express the vernacular names in a [VernacularName extension](http://rs.gbif.org/extension/gbif/1.0/vernacularname.xml). [[script](scripts/splitVernacularNames.py)]. Languages are mapped to their [ISO 639-3](http://en.wikipedia.org/wiki/ISO_639-3) code (the ISO 693-1 code as requested in `dwc:language` does not capture all languages). [[mapping file](documentation/language-mapping.tsv)] We also included the non-DwC term `_languageName`.
7. Express the traditional medicinal use in a [Description extension](http://rs.gbif.org/extension/gbif/1.0/description.xml). Currently, the full description includes parts, uses and sources, but is not marked up as HTML. We also included the non-DwC term `_plantPart`, which are reconciled. [[mapping file](documents/plant-parts-mapping.tsv)]
8. Add a `meta.xml` file. [[file](data/dwc-a/meta.xml)]
9. Catch up on sleep.
