import pandas as pd
from fuzzywuzzy import fuzz
import json
import os
import csv
import logging
from datetime import datetime
import enlighten
import re
import string


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
    return pd.read_csv(filepath, chunksize=chunksize, iterator=True, encoding="utf-8")


def combine_columns_as_str(df, fields, sep=" | "):
    global seperator
    seperator = sep

    fld = fields[0]
    out = df[fld].astype(str)
    for i, fld in enumerate(fields):
        if i > 0:
            out = out + sep + df[fld]
    return out.tolist()


def write_row(row, index, extra=None, filepath="output.csv"):
    global seperator
    row = row.split(seperator)
    row.insert(0, index)
    if extra:
        row.extend(extra.split(seperator))
    print(row, extra)
    if not os.path.exists(filepath):
        with open(filepath, 'a') as fp:
            pass    # create empty file

    if os.stat(filepath).st_size == 0:
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = fields["OUTPUT_FIELDS"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({fieldnames[i]: row[i] for i in range(len(fieldnames))})

    else:
        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = fields["OUTPUT_FIELDS"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({fieldnames[i]: row[i] for i in range(len(row))})


def filtersortfuzz(iterable, comparator, can_clean_text=True, cutoff=80):
    def cleanup_text(s):
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        s = regex.sub(' ', s)
        return re.sub(' +', ' ', s).strip()

    if can_clean_text:
        f = lambda x: fuzz.partial_ratio(cleanup_text(x).lower(), cleanup_text(comparator).lower())
    else:
        f = lambda x: fuzz.partial_ratio(x.lower(), comparator.lower())
    out = sorted(iterable, key=f, reverse=True)
    maxscore = f(out[0])
    return (comparator, out[0], maxscore) if maxscore >= cutoff else None    # FIX earlier was returning out[0] only


def main(verbose=False, no_log=False, skip_rows=0, skip_chunks=0, outputfile=None):
    FRS_filepath = fields["FRS_FILEPATH"]
    EIA_filepath = fields["EIA_FILEPATH"]

    log = not no_log
    if verbose:
        print("Reading file: ", FRS_filepath)
        print("Reading file: ", EIA_filepath)

    if log:
        logger.info("Reading file: %r", FRS_filepath)
        logger.info("Reading file: %r", EIA_filepath)

    FRS_iterator = read_in_chunks(FRS_filepath)
    # estimate size of chunk
    for df in FRS_iterator:
        sz = int(len(df.to_string()) / 2)   # dividing by 4 to get approx good chunk number
        fullsz = os.stat(FRS_filepath)
        break
    print("Chunk Size (B), Total size (B): ", sz, fullsz.st_size)

    num_iterations = fullsz.st_size // sz

    FRS_iterator = read_in_chunks(FRS_filepath)
    EIA_table = pd.read_csv(EIA_filepath, encoding="utf-8")   # read completely to memory
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

            if skip_rows > 0 and i < num_iter_to_skip:
                pbar.update()
                continue

            frs_chunk = frs_chunk.dropna()
            frs_items = combine_columns_as_str(frs_chunk, fields["FRS_FIELDS"])


            frs_indices = frs_chunk[fields["INDICES_FIELD"]].astype(str).tolist()
            eia_items = combine_columns_as_str(EIA_table, fields["EIA_FIELDS"])

            if start_after_index >= len(frs_items):
                start_after_index = 0
                continue    # dropna sometimes makes len < chunk_size
            if skip_rows > 0 and start_after_index > 0 and i == num_iter_to_skip:
                frs_items = frs_items[start_after_index:]
                frs_indices = frs_indices[start_after_index:]

            with enlighten.Counter(total=len(frs_items), desc='Processing Chunk {I}/{N}'.format(I=i, N=num_iterations), unit='ticks') as pbarmini:
                for index, item in zip(frs_indices, frs_items):
                    # p = process.extractOne(item, eia_items)
                    logger.info("%r", item)
                    p = filtersortfuzz(eia_items, item, cutoff=fields["FUZZ_THRESHOLD"])

                    # print("Input: {INP}\nMatch: {MAT}\n\n".format(INP=item, MAT=p))
                    if p:
                        if verbose: print("Input: {INP}\nMatch: {MAT}\n\n".format(INP=item, MAT=p))
                        if log: logger.info("Input: %r\nMatch: %r\n\n", item, p)
                        write_row(p[0], index, p[1], outputfile)
                    pbarmini.update()

            pbar.update()


if __name__ == "__main__":
    main()
