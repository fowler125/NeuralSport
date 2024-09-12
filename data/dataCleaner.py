"""
This file is designed to clean the data for preprocessing, for example:
    Drop NA Columns or empty columns
    Drop unecessary columns (Description, etc.)
"""

class dataCleaner:
    
    def __init__(self,id):
        self.id = id
    
    def open_file(self):
        print("This persons id is:",self.id)