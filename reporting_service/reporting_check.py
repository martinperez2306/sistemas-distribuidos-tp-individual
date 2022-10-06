import logging

class ReportingCheck:
    def __init__(self, service_instances):
        self.service_instances = service_instances
        self.funny_eofs = 0
        self.trending_eofs = 0
        self.max_eof = False
    
    def eof_funny(self):
        logging.info("Receive EOF of Funny")
        self.funny_eofs += 1
        logging.info("Funny EOFs [{}]".format(self.funny_eofs))

    def eof_trending(self):
        logging.info("Receive EOF of Trending")
        self.trending_eofs += 1
        logging.info("Trending EOFs [{}]".format(self.trending_eofs))

    def eof_max(self): 
        logging.info("Receive EOF of Max")
        self.max_eof= True

    def check_eofs(self):
        check = ((self.funny_eofs == self.service_instances) and (self.trending_eofs == self.service_instances) and self.max_eof)
        logging.info("Check [{}]".format(check))
        return check
