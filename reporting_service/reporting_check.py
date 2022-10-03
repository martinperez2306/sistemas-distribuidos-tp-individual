import logging

class ReportingCheck:
    def __init__(self, total_filter_checks):
        self.filter_checks = 0
        self.total_filter_checks = total_filter_checks
        self.grouper_check = False
    
    def check_filter(self):
        logging.info("Checking Filter")
        self.filter_checks += 1

    def check_grouper(self): 
        logging.info("Checking Grouper")
        self.grouper_check= True

    def check(self):
        logging.info("Check [{}]".format(((self.filter_checks == self.total_filter_checks) and self.grouper_check)))
        return ((self.filter_checks == self.total_filter_checks) and self.grouper_check)
