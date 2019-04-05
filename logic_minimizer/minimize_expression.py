from pyeda.inter import expr, espresso_exprs
from os import linesep

def minimize_rule(rule):
    """
    Given a rule in string form 'a | b & c',
    return (as strings)
        the espresso minimized form of the rule
        and the support (set of variables in the minimized rule)
    Why don't we just return the minimized rule? There can be problems
    converting the minimized rule back to an expression due to recursion depth.
    """
    f1 = expr(rule)
    if f1.is_one() or f1.is_zero():
        reduced_rule = str(bool(f1))
        return reduced_rule, set()
    else:
        f1_min, = espresso_exprs(f1.to_dnf())
        return str(f1_min), set(str(x) for x in f1_min.support)

def minimize_rule_and_save(rule, temp_file = 'temp_output.yml'):
    """
    Given a rule in string form 'a | b & c',
    write to file (as strings)
        the espresso minimized form of the rule
        #and the support (set of variables in the minimized rule)
    """
    print('Minimizing '+ rule)
    expression, support = minimize_rule(rule)
    support = str(list(support))
    with open(temp_file, 'w') as f:
        f.write('input_rule: ')
        f.write(rule)
        f.write(linesep)
        f.write('expression: ')
        f.write(expression)
        f.write(linesep)
        f.write('support: ')
        f.write(support)
    print('Minimized and saved')
    return None

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 3:
        rule = sys.argv[1]
        temp_file = sys.argv[2]
    else:
        sys.exit('Incorrect number of arguments passed. Please specify config file and temp file.')

    minimize_rule_and_save(rule, temp_file)