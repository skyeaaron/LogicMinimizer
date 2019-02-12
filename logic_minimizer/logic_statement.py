import helperfunctions as hf

class LogicStatement:
    """ 
    LogicStatement class represents logic statement strings.
    """
    def __init__(self, statement, form = 'verbose'):
        if form == 'verbose':
            self.verbose = statement
            self.rule = self.to_rule()
        elif form == 'rule':
            self.rule = statement
            self.verbose = self.to_verbose()
        self.type = self.classify()
        self.redundant_vars_verbose = None
        self.result = None
            
    def __repr__(self):
        return "<Verbose form:%s, Rule form: %s>, Type: %s" % (self.verbose, self.rule, self.type)
    
    def to_rule(self):
        return hf.input_to_rule(self.verbose)
    
    def to_verbose(self):
        return hf.rule_to_output(self.rule)
    
    def classify(self):
        return hf.suitable_check(self.rule)