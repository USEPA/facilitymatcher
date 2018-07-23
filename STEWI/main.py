import pandas as pd
import json
import os

with open("config.json") as cfg:
    fields = json.load(cfg)


if not fields:
    raise ValueError("No fields specified in config file")

if not "LOOKUP_FIELDS" in fields and fields["LOOKUP_FIELDS"]:
    raise ValueError("Not sure which fields to lookup in each row. Please update config.json with LOOKUP_FIELDS")

def is_duplicate(row):
    """
    Find if a row has duplicate values in specified fields
    :param row:
    :return:
    """

def main():

    if not fields["INCLUDE_ORIGINAL"] and not fields["KEEP_REPEATED_DUPLICATES"]:
        raise ValueError("Cannot have both INCLUDE_ORIGINAL and KEEP_REPEATED_DUPLICATES fields as False")

    datafilepath = fields["DATA_FILEPATH"]
    if os.path.splitext(datafilepath)[-1].lower() == ".csv":
        df = pd.read_csv(datafilepath)
    elif os.path.splitext(datafilepath)[-1].lower() == ".xlsx":
        df = pd.read_excel(datafilepath)
    output_csvfilepath = fields["OUTPUT_FILEPATH"]
    print("Starting processing data...")

    if fields["INCLUDE_ORIGINAL"]:
        keep = False
    else:
        keep = 'first'

    df_chunk_filtered = df[fields["LOOKUP_FIELDS"]]

    #df_chunk.loc[num_unique[num_unique == n].index].to_csv(output_csvfilepath, index=False, header=True, mode="w")
    #df_chunk.loc[num_unique[num_unique == n].index].to_csv(output_csvfilepath, index=False, header=False, mode="a", na_rep="NaN")

    if not fields["KEEP_REPEATED_DUPLICATES"]:
        df_dups = df[df_chunk_filtered.duplicated(keep=keep)]
        df_dups_filtered = df_dups[fields["LOOKUP_FIELDS"]]
        duplicates = df_dups[df_dups_filtered.duplicated(keep=keep).apply(lambda x: not x)]
        # print(duplicates)
        # make it have only unique duplicates
        # duplicates = df[duplicates.duplicated()]
    else:
        duplicates = df[df_chunk_filtered.duplicated(keep=keep)]

        # print(duplicates)
    duplicates.to_csv(output_csvfilepath, header=df.columns, index=False, mode='w')
    print("Process completed. Check the output file for results")




if __name__ == "__main__":
    main()