# -*- coding: utf-8 -*-
"""
Minimize logic statements
Takes a yaml config file specifying
    input_file (required)
    output_file (required)
    log_file (required)
    input_encoding (optional)
	max_variables (optional)
Input file:
    tab-delimited text file with headers
    first column contains statement identifiers
    second column contains logic statements in the form '(1 OR 2) AND 3'
    any other columns are ignored but will be included in the output

@author: SAaron
"""

#third-party modules
import sys
import yaml
from sympy import sympify, SympifyError
import sympy

#project modules
import helperfunctions as hf


"""
Load config_file and inputs
"""
#Take command line argument for config file, exit if none specified
if len(sys.argv) == 2:
    config_file = sys.argv[1]
else:
    sys.exit('Incorrect number of arguments passed. Please specify config file.')

with open(config_file, 'r') as f:
    config_dict = yaml.load(f)
    
input_file = config_dict['input_file']    
output_file = config_dict['output_file']
log_file = config_dict['log_file']
if 'input_encoding' in config_dict:
    input_encoding = config_dict['input_encoding']
else:
    input_encoding = 'utf-8'
if 'max_variables' in config_dict:
    max_variables = config_dict['max_variables']
else:
    max_variables = None
    
hf.create_log(log_file)

input_list, header = hf.csv_to_list(input_file, delimiter = '\t', encoding = input_encoding)

hf.print_and_log('input_file loaded', log_file)
hf.print_and_log('header = ' + str(header), log_file)
hf.print_and_log('using sympy version ' + sympy.__version__, log_file)

"""
Perform minimizations when possible

map each statement to list with 
    -reduced rule in input format '1 AND NOT 1 OR 2 AND NOT 2' 
    -redundant variables in input format as string '2, 1'
"""
#initialize dictionary with all unique logic statements
unique_logics = {row[1]: '' for row in input_list}

hf.print_and_log('Minimizing statements', log_file)

for statement in unique_logics:
    rule = hf.input_to_rule(statement)
    try:
        sympify(rule)
    except:
        reduced_rule_verbose = 'Error, expression could not be translated into logic statement.'
        redundant_variables_verbose = ''
        unique_logics[statement] = [reduced_rule_verbose, redundant_variables_verbose]
        continue
    else:
        try:
            starting_variables = set(str(x) for x in sympify(rule).free_symbols)
        except:
            hf.print_and_log(statement + ' failed on free_symbols', log_file)
            raise
        if max_variables is None:
            rule_min, ending_variables = hf.minimize_rule(rule)
        elif len(starting_variables) > max_variables:
            reduced_rule_verbose = 'Error, max variables exceeded.'
            redundant_variables_verbose = ''
            unique_logics[statement] = [reduced_rule_verbose, redundant_variables_verbose]
            continue
        else:
            rule_min, ending_variables = hf.minimize_rule(rule)
    redundant_variables = starting_variables - ending_variables
    redundant_variables_verbose = hf.letters_to_digits(', '.join(redundant_variables))
    try:
        reduced_rule = str(sympify(rule_min))
    except SympifyError as e:
        reduced_rule_verbose = 'Redundant variables calculated. Minimized expression cannot be parsed--probably too many terms.'
        hf.log('Error parsing minimized form of logic for rule: ' + statement, log_file)
        hf.log(str(e), log_file)
    else:
        reduced_rule_verbose = hf.rule_to_output(reduced_rule) #convert back to verbose form
    unique_logics[statement] = [reduced_rule_verbose, redundant_variables_verbose]

hf.print_and_log('Statements minimized', log_file)

"""
Save output_file
"""
output_header = header + ['Minimized Expression',
                          'Redundant Variables']

output = [output_header]
for row in input_list:
    output.append(row + unique_logics[row[1]])

hf.write_list_to_csv(output_file, output, delimiter = '\t')

hf.print_and_log('Output saved', log_file)
hf.print_and_log('Done', log_file)