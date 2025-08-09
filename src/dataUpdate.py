"""
Class: DataUpdate
Author: Zain Nomani
Description: Read in data from a csv file source and add current file to it. Remove duplicates. Write back to csv
"""

import pandas as pd

class DataUpdate:
    def __init__(self, source: str, data: list[list[str]], search: str):
        self.src = source
        self.search = search
        self.data = data
        self.currentDF: pd.DataFrame = None
        self.dataFrame: pd.DataFrame = None
        self.updatedDf: pd.DataFrame = None
    
    def run(self):
        self.clean()
        self.loadData()
        self.addToDF()
        self.writeToFile()
        return self

    def clean(self):
        new: list[str] = []
        for item in self.data:
            new.append(item[0]) # first link in result
        
        self.currentDF = pd.DataFrame({"url": new, "search": self.search})
        return self
    
    def loadData(self):
        dataFrame = pd.read_csv(self.src)
        self.dataFrame = dataFrame
        return self
    
    def addToDF(self):
        B = self.currentDF
        A = self.dataFrame
        unique_urls = B[~B['url'].isin(A['url'])]
        # Concatenate unique URLs to the existing DataFrame
        A = pd.concat([A, unique_urls], ignore_index=True)
        self.updatedDf = A

    def writeToFile(self):
        self.updatedDf.to_csv(self.src, index=False)
        return self