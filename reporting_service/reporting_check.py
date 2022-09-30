import logging

class ReportingCheck:
    def __init__(self):
        self.filter_check = False
        self.grouper_check = False
    
    def check_filter(self):
        logging.info("Checking Filter")
        self.filter_check = True

    def check_grouper(self): 
        logging.info("Checking Grouper")
        self.grouper_check= True

    def check(self):
        logging.info("Check [{}]".format(self.check_filter and self.check_grouper))
        return (self.filter_check and self.grouper_check)
