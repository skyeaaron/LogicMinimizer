# -*- coding: utf-8 -*-
"""
Module with functions for logic_minimizer.py

@author: SAaron
"""

import csv
import os
#from sympy import sympify, SympifyError
from pyeda.inter import expr, espresso_exprs


def csv_to_list(filename, header = True, delimiter = "\t", encoding = 'utf-8', quoting = csv.QUOTE_MINIMAL):
    """
    read delimited file
    if header is True then returns first row as header
    """
    with open(filename, 'r', encoding = encoding) as f:
        csv_f = csv.reader(f, delimiter = delimiter, quoting = quoting)
        if header:
            output_header = next(csv_f)
            output_data = [row for row in csv_f]
            return output_data, output_header
        else:
            output_header = None
            output_data= [row for row in csv_f]
            return output_data

def write_list_to_csv(filename, output, delimiter = '\t', newline = '\n'):
    """
    Save output list to csv
    """
    with open(filename, 'w+', newline = newline) as f:
        csv_f = csv.writer(f, delimiter = delimiter)
        csv_f.writerows(output)
    return None

def digits_to_letters(string):
    """
    given string containing digits, replace digits with letters
    """
    alphabet = {str(i-ord('a')): chr(i) for i in range(ord('a'), ord('k'))}
    new_string = string
    for key in alphabet:
        new_string = new_string.replace(key, alphabet[key])
    return new_string

def letters_to_digits(string):
    """
    given string containing letters, replace letters with digits
    """
    alphabet = {chr(i): str(i-ord('a')) for i in range(ord('a'),ord('k'))}
    new_string = string
    for key in alphabet:
        new_string = new_string.replace(key, alphabet[key])
    return new_string

def input_to_rule(statement):
    """
    Convert logic statements from numeric verbose format to sympy format
		e.g. format_as_logic('13 AND 2') = 'bd & c'
    Given a statement with criteria specified by numbers
    and logical operators in words,
    replace digits 0-9 with letters a-j
    and replace OR AND NOT with | & ~ 
	Case-insensitive
    """
    new_statement = statement.lower()
    new_statement = ('|').join(new_statement.split('or'))
    new_statement = ('&').join(new_statement.split('and'))
    new_statement = ('~').join(new_statement.split('not'))
    #replace digits with letters
    new_statement = digits_to_letters(new_statement)
    return new_statement

def rule_to_output(statement):
    """
    Given a logic statement formatted for sympy ('a | b & ~c')
    output a logic statement in Epic format.
    Replace letters with digits and operators with words.
    Special exception for expressions that are "True" or "False"
    """
    if statement=="True" or statement=="False":
        return statement
    new_statement = letters_to_digits(statement)
    new_statement = ('OR').join(new_statement.split('|'))
    new_statement = ('AND').join(new_statement.split('&'))
    new_statement = ('NOT ').join(new_statement.split('~'))
    return new_statement

def suitable_check(rule, max_variables, max_size):
    """
    given a string formatted as a | b
    run checks to make sure it is ok to try to minimize it
    """
    try:
        e = expr(rule, simplify=True)
        esup = e.support
    except:
        return 'Expression could not be translated into logic statement.'
    if len(esup) > max_variables:
        return 'Number of variables exceeds the max'
    try:
        dnf_size = e.to_dnf().size
    except:
        return 'Cannot convert to DNF'
    if dnf_size > max_size:
        return 'DNF is too big'
    if e.is_dnf():
        return None
    try:
        cnf_size = e.to_cnf().size
    except:
        return 'Cannot convert to CNF'
    if cnf_size > max_size:
        return 'CNF is too big'
    return None

def minimize_rule(rule):
    """
    Given a rule in string form 'a | b & c',
    return (as strings)
        the espresso minimized form of the rule
        and the support (set of variables in the minimized rule)
    """
    f1 = expr(rule)
    print(f1)
    if f1.is_one() or f1.is_zero():
        reduced_rule = str(bool(f1))
        return reduced_rule, set()
    else:
        f1_min, = espresso_exprs(f1.to_dnf())
        print('minimized')
        return str(f1_min), {str(x) for x in f1_min.support}


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
