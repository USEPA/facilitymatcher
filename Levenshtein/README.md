Introduction
============
This project is to match datasets using Fuzzy/Levenshtein algorithm 

Installation
============

This project requires the PyPy interpreter (v3.5) for faster processig. 
  
   Create a virtualenv
   
   $ virtualenv -p ~/pypy3 fuzzyEnv
   

Activate the environment:

$ source fuzzyEnv/bin/activate

On Windows, run

$ fuzzyEnv/Scripts/activate.bat

PIP installation:



$ ~/pypy3 -m ensurepip
 
Install project requirements:


   pip install -r requirements.txt
   
   Or if you are using the pypy interpreter directly
   
   ~/pip install -r requirements.txt
   
4. If any library fail to install

    ~/pip install --upgrade --force-reinstall library_name
    

Usage
=====


$ ~/pypy3 cli.py --help

Usage: cli.py [OPTIONS]

  A tool that compares two CSV files and finds matches based on input
  fields.

Use config.json  for FRS filepath, EIA filepath, the
  fields  to match, threshold to be set, chunk_size

  chunksize refers to how much of the FRS file is read per iteration. If you
  have a large RAM, you can increase chunksize and speed up processing
  slightly.

Options:
  --verbose              Produces program logs, slows down the program
                         considerably
  --no-log TEXT          Skip logging the current run of the program
  --skip-rows INTEGER    Given an integer count {N}, skips N rows of first
                         input file for processing. Used when an output is
                         already partially created and you wish to continue a
                         broken process
  --skip-chunks INTEGER  Given an integer count {N}, skips first N chunks,
                         based on chunksize in config.json. Used when an
                         output is already partially created and you wish to
                         continue a broken process
  --output TEXT          Output file path
  --help                 Show this message and exit.

To run the app 

$ ~/pypy3 cli.py --verbose

This uses the default output filepath of "./output.csv" in current directory and prints in a verbose manner any matches
found and how much of the processing is complete.

Checklist
============

1. Is  virtual environment activated
2. In the python interpreter linked to the project, is all the libraries installed
If not try:
`pip install -r requirements.txt`
3. if you get  warning of Python-Levenshtein not installed, try
`pip install --upgrade --force-reinstall python-Levenshtein`

4. Pandas issue. If you are using a python interpreter with pandas preinstalled, pandas might be in the latest version
pandas>0.20 doesn't work well with PyPy, you can reinstall pandas like this 

`pip install --upgrade --force-reinstall pandas==0.20`