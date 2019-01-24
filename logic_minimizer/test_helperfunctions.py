# -*- coding: utf-8 -*-
from helperfunctions import input_to_rule, suitable_check


def test_input_to_rule_digits():
    assert input_to_rule('55') == 'ff'
 
def test_input_to_rule_spaces():
    assert input_to_rule(' OR ') == '|'
    
def test_suitable_check_andornot():
    assert suitable_check('|', 0, 0) == 'And/Or/Not'