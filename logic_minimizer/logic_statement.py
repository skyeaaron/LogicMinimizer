#project modules
import format_expressions as fe

class LogicStatement:
    """ 
    LogicStatement class represents logic statement strings.
    Verbose is in the form 1 AND 2 OR NOT 3
    Rule is in the form a & b | ~c
    """
    def __init__(self, statement, form = 'verbose', nots = '~'):
        self.nots = nots
        if form == 'verbose':
            self.verbose = statement
            self.rule = self.to_rule()
        elif form == 'rule':
            self.rule = statement
            self.verbose = self.to_verbose()
        self.type = self.classify()
        self.rule_min = None #minimized form of rule
        self.rule_min_variables = None #variables in minimized rule -- set and not calculated
        self.result = None
            
    def __repr__(self):
        return "<Verbose form:%s, Rule form: %s>, Type: %s" % (self.verbose, self.rule, self.type)
    
    def to_rule(self):
        return fe.input_to_rule(self.verbose, nots = self.nots)
    
    def to_verbose(self):
        return fe.rule_to_output(self.rule, nots = self.nots)
    
    def classify(self):
        return fe.categorize_rule(self.rule)
    
    def update_result(self):
        """ Default result is N/A.
        Sets result to True, False, Redundancy, No redundancy, or N/A
        """
        if self.rule_min == 'True':
            self.result = 'Always True'
        elif self.rule_min == 'False':
            self.result = 'Always False'
        elif self.redundant_variables == '':
            self.result = 'No Redundancy'
        elif self.redundant_variables != 'N/A':
            self.result = 'Redundancy'
        else:
            self.result = 'N/A'
    
    @property
    def variables(self):
        """ return any variables used in the rule """
        return fe.variables(self.rule)
    
    @property
    def redundant_variables(self):
        """ 
        return string listing any variables in rule but not in min_rule 
        return N/A if either rule_min or rule_min_variables is None 
        '1,2,3'
        """
        if self.rule_min_variables is None:
            return 'N/A'
        else:
            return ', '.join(fe.variables_to_digits(self.variables - self.rule_min_variables))