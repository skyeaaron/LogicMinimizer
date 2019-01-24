from pyeda.inter import expr, espresso_exprs

#from sys import argv
#rule = argv[1]

def minimize_rule(rule):
    """
    Given a rule in string form 'a | b & c',
    return (as strings)
        the espresso minimized form of the rule
        and the support (set of variables in the minimized rule)
    """
    print('commence')
    f1 = expr(rule)
    if f1.is_one() or f1.is_zero():
        reduced_rule = str(bool(f1))
        expression = reduced_rule
        support = set()
    else:
        print('to dnf')
        dnf_form = f1.to_dnf()
        print('in dnf')
        print('minimizing')
        f1_min, = espresso_exprs(dnf_form)
        print('minimized')
        expression = str(f1_min)
        support = {str(x) for x in f1_min.support}
    with open("test_output.txt", 'w') as f:
        f.write('expression: ')
        f.write(expression)
        f.write('\n')
        f.write('support: ')
        f.write(str(support))
    return None

