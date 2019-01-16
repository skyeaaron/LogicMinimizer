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
from sympy import sympify
#import sympy
from pyeda.inter import expr





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
    max_variables = 55
if 'max_size' in config_dict:
    max_size = config_dict['max_size']
else:
    max_size = 10000
    
hf.create_log(log_file)

input_list, header = hf.csv_to_list(input_file, delimiter = '\t', encoding = input_encoding)

hf.print_and_log('input_file loaded', log_file)
hf.print_and_log('header = ' + str(header), log_file)
hf.print_and_log('max size = ' + str(max_size), log_file)
hf.print_and_log('max variables = ' + str(max_variables), log_file)
#hf.print_and_log('using sympy version ' + sympy.__version__, log_file)

"""
Perform minimizations when possible

map each statement to list with 
    -reduced rule in input format '1 AND NOT 1 OR 2 AND NOT 2' 
    -redundant variables in input format as string '2, 1'
"""
#initialize dictionary with all unique logic statements
unique_logics = {row[1]: '' for row in input_list}

hf.print_and_log('Minimizing statements', log_file)

total = len(unique_logics)
count = -1

for statement in unique_logics:
    count +=1
    if not count % 10:
        print('processing statement ' + str(count) + ' of ' + str(total))
    rule = hf.input_to_rule(statement)
    print('checking ' + statement)
    check = hf.suitable_check(rule, max_variables, max_size)
    if check is not None:
        print(statement, check)
        unique_logics[statement] = [check, '']
        continue
    starting_variables = set(str(x) for x in expr(rule, simplify=False).support)
    print('minimizing ' + statement)
    rule_min, ending_variables = hf.minimize_rule(rule)
    redundant_variables = starting_variables - ending_variables
    redundant_variables_verbose = hf.letters_to_digits(', '.join(redundant_variables))
    try:
        print('try to sympify')
        reduced_rule = str(sympify(rule_min))
    except Exception as e:
        reduced_rule_verbose = 'Redundant variables calculated. Minimized expression cannot be displayed.'
        hf.log('Error parsing minimized form of logic for rule: ' + statement, log_file)
        hf.log(str(e), log_file)
    else:
        print('sympified')
        reduced_rule_verbose = hf.rule_to_output(reduced_rule) #convert back to verbose form
    unique_logics[statement] = [reduced_rule_verbose, redundant_variables_verbose]
    print('did it onto the next')

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