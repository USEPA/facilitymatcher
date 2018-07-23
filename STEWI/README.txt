Duplicates Finder
=================

Edit `config.json`. Here is an example

```
{
  "DATA_FILEPATH": "data/StewiComboInput.xlsx",
  "LOOKUP_FIELDS": ["FacilityID", "Compartment", "SRS_ID"],
  "OUTPUT_FILEPATH": "output.csv",
  "KEEP_REPEATED_DUPLICATES": true,
  "INCLUDE_ORIGINAL": true
}
```

 "DATA_FILEPATH" is the input data csv/xlsx file path
 "LOOKUP_FIELDS" are the columns in input that are compared. If in any row all the values under these columns are same, then that row is written to the output file.
 "OUTPUT_FILEPATH" is the output data csv file path (Only CSV outputs are coded, No XLSX)
"KEEP_REPEATED_DUPLICATES" set to true would keep all matches found for a original set
"INCLUDE_ORIGINAL" will keep the original set as well

run:

python main.py

or

python3 main.py