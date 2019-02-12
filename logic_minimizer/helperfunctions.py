# -*- coding: utf-8 -*-
"""
Module with functions for logic_minimizer.py
"""

import csv
import os
from pyeda.inter import expr

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
    new_statement = new_statement.strip()
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

def suitable_check(rule):
    """
    given a string formatted as a | b
    run checks to make sure it is ok to try to minimize it
    """
    try:
        e = expr(rule, simplify=True)
        esup = e.support
    except:
        if rule == '|' or rule == '&' or rule == '~':
            return 'And/Or/Not'
        elif 'at least' in rule.lower() or 'at most' in rule.lower() or 'exactly' in rule.lower():
            return 'At least/At most/Exactly'
        else:
            return 'Invalid statement'
    if len(esup) > 30:
        return 'Big statement'
    return 'Small statement'


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
