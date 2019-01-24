# -*- coding: utf-8 -*-
"""
Troubleshooting python crash on large statements

@author: SAaron
"""

#import sys
#import yaml
#from sympy import sympify
#from pyeda.inter import expr
#from subprocess import check_output
from minimize import minimize_rule
#import time
from multiprocessing import Process
import helperfunctions as hf
#from multiprocessing import cpu_count
#import subprocess
import psutil
from time import sleep
#import resource

#
#
if __name__ == '__main__':
    logfile = 'rule_min_log.txt'
    hf.create_log(logfile)
    rule = '(1 OR 2 OR 3 OR 4 OR 5 OR 6 OR 7 OR 8 OR 9 OR 10 OR 11 OR 12 OR 13 OR 14 OR 15 OR 16 OR 17) AND (18 OR 19 OR 20 OR 21 OR 22 OR 23 OR 24 OR 25 OR 26 OR 27 OR 28 OR 29 OR 30 OR 31 OR 32 OR 33 OR 34) AND ((18 AND 35 AND 36 AND 37 AND 38) OR (19 AND 39 AND 40 AND 41 AND 42) OR (20 AND 43 AND 44 AND 45 AND 46) OR (21 AND 47 AND 48 AND 49 AND 50) OR (22 AND 51 AND 52 AND 53 AND 54) OR (23 AND 55 AND 56 AND 57 AND 58) OR (24 AND 59 AND 60 AND 61 AND 62) OR (25 AND 63 AND 64 AND 65 AND 66) OR (26 AND 67 AND 68 AND 69 AND 70) OR (27 AND 71 AND 72 AND 73 AND 74) OR (28 AND 75 AND 76 AND 77 AND 78) OR (29 AND 79 AND 80 AND 81 AND 82) OR (30 AND 83 AND 84 AND 85 AND 86) OR (31 AND 87 AND 88 AND 89 AND 90) OR (32 AND 91 AND 92 AND 93 AND 94) OR (33 AND 95 AND 96 AND 97 AND 98) OR (34 AND 99 AND 100 AND 101 AND 102))'
    #rule = '1 or 2'
    rule = hf.input_to_rule(rule)
    hf.print_and_log('using rule :' + rule, logfile)

#    minimize_rule(rule)
#    print(resource.getrusage(0))
    p = Process(target=minimize_rule, args=(rule,))
    hf.print_and_log('process created', logfile)
    p.start()
    hf.print_and_log('process started', logfile)
    #p.join(20)
    while psutil.virtual_memory().percent <= 90:
        if not p.is_alive():
            hf.print_and_log('p is no longer alive', logfile)
            break
        else:
            hf.print_and_log(str(psutil.virtual_memory()), logfile)
            hf.print_and_log(str(psutil.swap_memory()), logfile)
            sleep(1)
           # print(resource.getrusage(0))
    if p.is_alive():
        p.terminate()
    if not p.is_alive():
        print('terminated')
    p.join()
    hf.print_and_log('we made it to the end', logfile)

