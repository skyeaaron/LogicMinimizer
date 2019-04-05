from format_expressions import input_to_rule, categorize_rule


def test_input_to_rule_digits():
    assert input_to_rule('55') == 'ff'
 
def test_input_to_rule_spaces():
    assert input_to_rule(' OR ') == '|'
    
def test_categorize_rule_andornot():
    assert categorize_rule('|', 0, 0) == 'And/Or/Not'