class ReportingCheck:
    def __init__(self):
        self.filter_check = False
        self.grouper_check = False
    
    def check_filter(self):
        self.filter_check = True

    def check_grouper(self): 
        self.grouper_check= True

    def check(self):
        return (self.check_filter and self.check_grouper)
