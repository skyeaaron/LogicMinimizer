# -*- coding: utf-8 -*-
"""
Minimize logic statements
Takes a yaml config file specifying
    input_file (required, WITH HEADERS)
    output_file (required)
    log_file (required)
    temp_file (required for storing output of large expressions)
    input_encoding (optional)
    timeout (optional, max seconds to spend on a big statement)
Input file:
    tab-delimited text file with headers
    first column contains statement identifiers
    second column contains logic statements in the form '(1 OR 2) AND 3'
    any other columns are ignored but will be included in the output
"""

#third-party modules
import sys
import yaml
import subprocess
import logging
from os import linesep
from time import time

#project modules
import processfiles as pf
import logic_statement as l
from minimize_expression import minimize_rule

start_time = time()

"""
Load config_file and inputs
"""
#Take command line argument for config file, exit if none specified
if len(sys.argv) == 2:
    config_file = sys.argv[1]
else:
    sys.exit('Incorrect number of arguments passed. Please specify config file.')


"""
Load settings from config file
"""
with open(config_file, 'r') as f:
    config_dict = yaml.safe_load(f)
    
input_file = config_dict['input_file']    
output_file = config_dict['output_file']
temp_file = config_dict['temp_file']
log_file = config_dict['log_file']
if 'input_encoding' in config_dict:
    input_encoding = config_dict['input_encoding']
else:
    input_encoding = 'utf-8'
if 'timeout' in config_dict:
    timeout = config_dict['timeout']
else:
    timeout = None

logging.basicConfig(filename=log_file, filemode = 'w', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
logging.info('Log file created')
logging.info('Start time: ' + str(start_time))

"""
import data
"""
input_list, header = pf.csv_to_list(input_file, delimiter = '\t', encoding = input_encoding)

logging.info('input_file loaded')
logging.info('header = ' + str(header))

"""
Initialize temp_file where big statements are stored
"""
try:
    with open(temp_file, 'w') as f:
        f.write('input_rule:'+linesep+'expression:'+linesep+'support:'+linesep)
except:
    logging.exception("Failed to create temp_file for storing big statement outputs.")
    raise


"""
Perform minimizations when possible

For each statement, we categorize the rule.
We perform espresso minimization when possible.
For big statements we perform minimiziation in a separate subprocess
so that the parent process can survive even if there is a segfault.
We will save:
    -type: Big, Small, At least/At most/Exactly, error message
    -result: True, False, Redundancy, Error Message, N/A 
    -redundant variables: in input format as string '2, 1' or '' or 'N/A'
"""
#get all unique logic statements
unique_statements = set(row[1] for row in input_list)
#intialize dictionary of LogicStatements indexed by their string form
ulogics = {x: l.LogicStatement(x, 'verbose') for x in unique_statements}

pf.print_and_log('Minimizing statements', log_file)

#loop through all statements s in ulogics
for s in ulogics:
    logging.info("Minimizing " + s)
    logging.info(ulogics[s].type)
    #for small statements, minimize within the main process
    if ulogics[s].type == 'Small statement':        
        ulogics[s].rule_min, ulogics[s].rule_min_variables = minimize_rule(ulogics[s].rule)
        ulogics[s].update_result()
        logging.info(ulogics[s].result)
    elif ulogics[s].type == 'Big statement':
        try:
            sub_result = subprocess.check_output(["python", "minimize_expression.py", ulogics[s].rule, temp_file], timeout = timeout)
            logging.info("Subprocess result:" + linesep + sub_result.decode("utf-8").strip() + linesep + "End of subprocess result.")
        except subprocess.TimeoutExpired:
            logging.exception("Subprocess exceeded timeout. Expression was not minimized.")
            ulogics[s].result = "Subprocess exceeded timeout. Expression was not minimized."
            logging.info(ulogics[s].result)
            continue
        except subprocess.CalledProcessError:
            logging.exception('Subprocess returned a non-zero exit code. Expression was not minimized.')
            ulogics[s].result = 'Subprocess returned a non-zero exit code. Expression was not minimized.'
            logging.info(ulogics[s].result)
            continue
        with open(temp_file, 'r') as f:
            sub_output = yaml.safe_load(f)
        if ulogics[s].rule != sub_output['input_rule']:
            #if for any reason the temp file does not contain the current rule,
            #record this in the result and go to the next rule
            ulogics[s].result = 'Wrong rule found in temp file, suggesting issue with the subprocess or temp file. Check log.'
            logging.info(ulogics[s].result)
            continue
        else:
            ulogics[s].rule_min = sub_output['expression']
            ulogics[s].rule_min_variables = set(x for x in sub_output['support'])
            ulogics[s].update_result()
            logging.info(ulogics[s].result)
    else:
        ulogics[s].result = 'N/A'
        logging.info(ulogics[s].result)
        
logging.info('Statements minimized')

"""
Save output_file
"""
output_header = header + ['Type',
                          'Redundant Variables', 
                          'Result']

output=[output_header]
for row in input_list:
    output.append(row +
                   [ulogics[row[1]].type, 
                   ulogics[row[1]].redundant_variables, 
                   ulogics[row[1]].result])

pf.write_list_to_csv(output_file, output, delimiter = '\t')

logging.info('Output saved')

end_time = time()
logging.info('End time: ' + str(end_time))
logging.info('Total time in seconds: ' + str(end_time-start_time))

"""
Count number of each result
"""
counts = dict()
for row in output[1:]:
  counts[row[-1]] = counts.get(row[-1], 0) + 1
  
logging.info('Counts of each result:\n' + '\n'.join([key + ': ' + str(counts[key]) for key in counts]))