"""
Date: 17/8/2025
Description: Interact with MongoDB to retrieve and update records as needed
"""

import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import pandas as pd

class Database:
    """
    Connection to MongoDB Database and load to Pandas
    """
    def __init__(self): # initialise connection to DB
        load_dotenv()
        uri = os.getenv("MONGODBURI")
        self.uri = uri
        self.df = None

    def getDb(self): # Retrieve information from database
        client = MongoClient(self.uri)
        db = client["test"]["Leads"]
        cursor = db.find({}, {"_id": 0})
        df = pd.DataFrame(list(cursor))[["name", "headline", "location", "link", "model", "actual"]]
        self.df = df
        client.close()
        return df

    def update(self, filter: dict, replacement: dict): # Update record
        """
        filter: {"field": "value"}
        replacement: {"name": name, "link": link}
        """
        try:
            client = MongoClient(self.uri)
            collection = client["test"]["Leads"]
            result = collection.replace_one(filter, replacement)
            self.getDb()
            client.close()
            return result.modified_count > 0
        except Exception as e:
            raise Exception("Unable to edit document due to the following error: ", e)