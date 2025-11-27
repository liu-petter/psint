class PSDict:
    """PostScript dictionary"""
    def __init__(self):
        self.dict = {}

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]
    
    def __contains__(self, key):
        return key in self.dict
    
    def __repr__(self):
        return f"PSDICT({self.dict})"
    
    def __str__(self):
        return f"PSDICT({self.dict})"