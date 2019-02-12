# -*- coding: utf-8 -*-
"""
Minimize logic statements
Takes a yaml config file specifying
    input_file (required)
    output_file (required)
    log_file (required)
    temp_file (required for storing output of large expressions)
    input_encoding (optional)
    vm_limit (optional, percent increase cap on virtual memory)
Input file:
    tab-delimited text file with headers
    first column contains statement identifiers
    second column contains logic statements in the form '(1 OR 2) AND 3'
    any other columns are ignored but will be included in the output
"""

#third-party modules
import sys
import yaml
from pyeda.inter import expr
from multiprocessing import Process, freeze_support
import psutil
from time import sleep

#project modules
import helperfunctions as hf
import logic_statement as l
from minimize import minimize_rule_and_save, minimize_rule


"""
Load config_file and inputs
"""
if __name__ == '__main__':
    freeze_support()
    #Take command line argument for config file, exit if none specified
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    else:
        sys.exit('Incorrect number of arguments passed. Please specify config file.')
    
    #config_file = '..\\SampleFiles\\SampleLogicFile_Config.yml'
    
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
    if 'vm_limit' in config_dict:
        vm_limit = config_dict['vm_limit']
    else:
        vm_limit = 15
        
    hf.create_log(log_file)
    
    hf.print_and_log('test', log_file)
    
    input_list, header = hf.csv_to_list(input_file, delimiter = '\t', encoding = input_encoding)
    
    hf.print_and_log('input_file loaded', log_file)
    hf.print_and_log('header = ' + str(header), log_file)
    
    """
    Perform minimizations when possible
    
    map each statement to list with 
        -reduced rule in input format '1 AND NOT 1 OR 2 AND NOT 2' 
        -redundant variables in input format as string '2, 1'
    """
    #initialize dictionary with all unique logic statements
    unique_statements = set(row[1] for row in input_list)
    ulogics = {x: l.LogicStatement(x, 'verbose') for x in unique_statements}
    
    hf.print_and_log('Minimizing statements', log_file)
    
    #loop through all statements s in ulogics
    for s in ulogics:
        if ulogics[s].type == 'Small statement':
            starting_variables = set(str(x) for x in expr(ulogics[s].rule, simplify=False).support)
            rule_min, ending_variables = minimize_rule(ulogics[s].rule)
            redundant_variables = starting_variables - ending_variables
            ulogics[s].redundant_vars_verbose = hf.letters_to_digits(', '.join(redundant_variables))
            if rule_min in ('True', 'False'):
                ulogics[s].result = rule_min
            elif redundant_variables:
                ulogics[s].result = 'Redundancy'
            else:
                ulogics[s].result = 'No redundancy'
        elif ulogics[s].type == 'Big statement':
            starting_variables = set(str(x) for x in expr(ulogics[s].rule, simplify=False).support)
            p = Process(target = minimize_rule_and_save, 
                        args=(ulogics[s].rule, temp_file,))
            p.start()
            hf.print_and_log('process started', log_file)
            starting_vm = psutil.virtual_memory().percent
            hf.print_and_log('starting_vm = ' + str(starting_vm), log_file)
            while p.is_alive() and psutil.virtual_memory().percent <= starting_vm + vm_limit:
                hf.print_and_log(str(psutil.virtual_memory()), log_file)
                sleep(1)
            if p.is_alive():
                p.terminate()
                hf.print_and_log('p was terminated. rule could not be minimized', log_file)
                sleep(1)
                if p.is_alive():
                    hf.print_and_log('process did not terminate properly', log_file)
                ulogics[s].result = 'Too large to minimize'
                ulogics[s].redundant_vars_verbose = 'N/A'
            else:
                hf.print_and_log('p is not alive', log_file)
                with open(temp_file, 'r') as f:
                    process_output = yaml.safe_load(f)
                if ulogics[s].rule != process_output['input_rule']:
                    #if for any reason the temp file does not contain the current rule,
                    #record as too big to minimize and go to the next rule
                    ulogics[s].result = 'Wrong rule. Too large to minimize?'
                    ulogics[s].redundant_vars_verbose = 'N/A'
                    continue
                rule_min = process_output['expression']
                ending_variables = set(process_output['support'])
                redundant_variables = starting_variables - ending_variables
                ulogics[s].redundant_vars_verbose = hf.letters_to_digits(', '.join(redundant_variables))
                if rule_min in ('True', 'False'):
                    ulogics[s].result = rule_min
                elif redundant_variables:
                    ulogics[s].result = 'Redundancy'
                else:
                    ulogics[s].result = 'No redundancy'
            p.join()
        else:
            ulogics[s].redundant_vars_verbose = 'N/A'
            ulogics[s].result = 'N/A'
    
    hf.print_and_log('Statements minimized', log_file)
    
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
                       ulogics[row[1]].redundant_vars_verbose, 
                       ulogics[row[1]].result])
    
    hf.write_list_to_csv(output_file, output, delimiter = '\t')
    
    hf.print_and_log('Output saved', log_file)
    hf.print_and_log('Done', log_file)