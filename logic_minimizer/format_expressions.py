# -*- coding: utf-8 -*-
"""
For converting between 1 and 2 form and a & b form
For checking whether statements are small/big/invalid
For getting the list of variables
"""

from pyeda.inter import expr

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

def input_to_rule(statement, nots = '~'):
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
    new_statement = (nots).join(new_statement.split('not'))
    #replace digits with letters
    new_statement = digits_to_letters(new_statement)
    new_statement = new_statement.strip()
    return new_statement

def rule_to_output(statement, nots = '~'):
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
    new_statement = ('NOT ').join(new_statement.split(nots))
    return new_statement

def categorize_rule(rule):
    """
    given a string formatted as a | b
    run checks to make sure it is ok to try to minimize it
    sort it into a category
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

def variables(rule):
    """
    given a string formatted as a | b
    return a set of the variables as strings
    """
    if rule in ('True', 'False'):
        return set()
    else:
        return set(str(x) for x in expr(rule, simplify=False).support)

def variables_to_digits(variables):
    """
    given a set of variables {'a', 'b', 'aa'}
    return them as digits {'0', '1', '00'}
    """
    return set(letters_to_digits(x) for x in variables)
    