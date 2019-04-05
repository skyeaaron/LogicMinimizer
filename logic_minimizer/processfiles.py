# -*- coding: utf-8 -*-
"""
Module with functions for logic_minimizer.py
Read and write csv
Create simple logs
"""

import csv
import os

def csv_to_list(filename, header = True, delimiter = '\t', encoding = 'utf-8', quoting = csv.QUOTE_MINIMAL):
    """
    read delimited file
    if header is True then returns first row as header
    """
    with open(filename, 'r', encoding = encoding) as f:
        csv_f = csv.reader(f, delimiter = delimiter, quoting = quoting)
        if header:
            output_header = next(csv_f)
            return list(csv_f), output_header
        else:
            return list(csv_f)

def write_list_to_csv(filename, output, delimiter = '\t', newline = '\n'):
    """
    Save output list to csv
    """
    with open(filename, 'w+', newline = newline) as f:
        csv_f = csv.writer(f, delimiter = delimiter)
        csv_f.writerows(output)
    return None

def create_log(logfilename):
    """
    overwrite or create logfile
    """
    with open(logfilename, 'w+') as f:
        f.write('log file created' + os.linesep)

def log(message, logfilename):
    """
    write message to log file
    """
    with open(logfilename, 'a') as f:
        f.write(message + os.linesep)
    return None

def print_and_log(message, logfilename):
    """
    print message, and
    write message to log file
    """
    print(message)
    log(message, logfilename)
    return None