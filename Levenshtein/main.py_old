import pandas as pd
from fuzzywuzzy import fuzz
import json
import os
import csv
import logging
from datetime import datetime
import enlighten


seperator = " | "
log = True
verbose = True

with open("config.json") as cfg:
    fields = json.load(cfg)

if not os.path.exists("logs"):
    os.mkdir("logs")

if not os.path.isdir("logs"):
    raise NotADirectoryError("logs/ must be a directory. Please fix in the current directory of this program")

if log:
    # logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    fh = logging.FileHandler(os.path.join("logs", datetime.now().strftime('log_%H_%M_%d_%m_%Y.log')))
    fh.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)


def read_in_chunks(filepath):
    chunksize = fields["CHUNK_SIZE"]
    return pd.read_csv(filepath, chunksize=chunksize, iterator=True)


def combine_columns_as_str(df, fields, sep=" | "):
    global seperator
    seperator = sep

    fld = fields[0]
    out = df[fld].astype(str)
    for i, fld in enumerate(fields):
        if i > 0:
            out = out + sep + df[fld]
    return out.tolist()


def write_row(row, filepath="output.csv"):
    global seperator
    row = row.split(seperator)

    if not os.path.exists(filepath):
        with open(filepath, 'a') as fp:
            pass    # create empty file

    if os.stat(filepath).st_size == 0:
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = fields["OUTPUT_FIELDS"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({fieldnames[i]: row[i] for i in range(len(row))})

    else:
        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = fields["OUTPUT_FIELDS"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({fieldnames[i]: row[i] for i in range(len(row))})


def filtersortfuzz(iterable, comparator, cutoff=80):
    # f = lambda x: fuzz.ratio(x, comparator)
    # f = lambda x: fuzz.partial_token_sort_ratio(x, comparator, force_ascii=True)
    f = lambda x: fuzz.partial_ratio(x.lower(), comparator.lower())
    # f = lambda x: 100*jellyfish.jaro_distance(x.lower(), comparator.lower())
    out = sorted(iterable, key=f, reverse=True)
    maxscore = f(out[0])
    return (out[0], maxscore) if maxscore >= cutoff else None


def main(verbose=False, no_log=False, skip_rows=0, skip_chunks=0, outputfile=None):
    FRS_filepath = fields["FRS_FILEPATH"]
    EIA_filepath = fields["EIA_FILEPATH"]
    # print("EIA Type", type(EIA_filepath))
    log = not no_log
    if verbose:
        print("Reading file: ", FRS_filepath)
        print("Reading file: ", EIA_filepath)

    if log:
        logger.info("Reading file: " + FRS_filepath)
        logger.info("Reading file: " + EIA_filepath)

    FRS_iterator = read_in_chunks(FRS_filepath)
    # estimate size of chunk
    for df in FRS_iterator:
        sz = len(df.to_string())
        fullsz = os.stat(FRS_filepath)
        break
    print("Chunk Size (B), Total size (B): ", sz, fullsz.st_size)

    num_iterations = fullsz.st_size // sz

    FRS_iterator = read_in_chunks(FRS_filepath)
    EIA_table = pd.read_csv(EIA_filepath)   # read completely to memory
    EIA_table = EIA_table.dropna()

    num_iter_to_skip = 0
    start_after_index = 0
    if skip_rows > 0:
        num_iter_to_skip = skip_rows // fields["CHUNK_SIZE"]
        start_after_index = skip_rows - (num_iter_to_skip*fields["CHUNK_SIZE"])

    if skip_chunks > 0:
        num_iter_to_skip = skip_chunks

    with enlighten.Counter(total=num_iterations, desc='Progress...', unit='ticks') as pbar:
        print("Starting comparisons...")
        for i, frs_chunk in enumerate(FRS_iterator):
            frs_chunk = frs_chunk.dropna()
            if skip_rows > 0 and i < num_iter_to_skip: continue
            frs_items = combine_columns_as_str(frs_chunk, fields["FRS_FIELDS"])
            eia_items = combine_columns_as_str(EIA_table, fields["EIA_FIELDS"])

            eia_items = eia_items[:10] # DEBUG FIXME
            if skip_rows > 0 and start_after_index > 0 and i == num_iter_to_skip:
                frs_items = frs_items[frs_items.length > start_after_index]
            # print(eia_items[:10])
            with enlighten.Counter(total=len(frs_items), desc='Processing Chunk {I}/{N}'.format(I=i, N=num_iterations), unit='ticks') as pbarmini:
                for item in frs_items:
                    # p = process.extractOne(item, eia_items)
                    logger.info(item)
                    p = filtersortfuzz(eia_items, item, fields["FUZZ_THRESHOLD"])
                    # print("Input: {INP}\nMatch: {MAT}\n\n".format(INP=item, MAT=p))
                    if p:
                        if verbose: print("Input: {INP}\nMatch: {MAT}\n\n".format(INP=item, MAT=p))
                        if log: logger.info("Input: {INP}\nMatch: {MAT}\n\n".format(INP=item, MAT=p))

                        write_row(p[0], outputfile)
                    pbarmini.update()

            pbar.update()

            # break


if __name__ == "__main__":
    # open file1 csv
    FRS_filepath = "data/FRS_Facility.csv"
    EIA_filepath = "data/EIAinventoryfacilitytable.csv"

    # main(FRS_filepath, EIA_filepath)