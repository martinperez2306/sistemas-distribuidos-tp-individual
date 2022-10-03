class Propagation:
    def __init__(self):
        self.starts_count = 0
        self.ends_count = 0

    def inc_start(self):
        self.starts_count += 1
    
    def inc_end(self):
        self.ends_count += 1