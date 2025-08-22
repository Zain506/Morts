"""
Date: 21/8/2025
Description: Model class which generates embeddings for Pandas series. Integrates into Streamlit
"""

import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
# Load a model specifically trained for sentence embeddings

class Model:
    """
    Require a pandas series of texts and outputs the 
    """
    def __init__(self):
        self.model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")
        self.samples = None
    
    def run(self, text: pd.Series) -> pd.Series:
        """Run start to finish from a series of texts to a series of true or false"""
        embeddings = self._genEmbeddings(text)
        self._getProf()
        similarity = self._calcSim(embeddings)
        classes = self._classify(similarity)
        return self._construct(classes)


    def _genEmbeddings(self, text: pd.Series) -> np.ndarray:
        # Refactor the dataframe into an array of strings then feed self.model.encode(array_of_strings)
        text = text.reset_index(drop=True)

        return self.model.encode(text)

    def _getProf(self) -> np.ndarray:
        # Provie 2 example profiles, generate embeddings and store in array
        # Used to dot product and find cosine similarity with other data points
        true: str = """
Name: Julian Cross
Location: London, UK
Headline: London-based C-Level Executive | Driving Operational Excellence & Strategic Growth | Helping Businesses scale with purpose
"""
        false: str = """
Name: Chloe Wilson
Location: California, USA
Headline: Gender Studies student at Santa Monica College | Focussed on social justice advocacy and community organising | Pet lover
"""
        comp: np.ndarray = np.array([self.model.encode(true), self.model.encode(false)])
        self.samples = comp
        return comp

    def _calcSim(self, embeddings: np.ndarray) -> np.ndarray:
        # Apply dot product to cosine similarity then softmax with 2 other pre-calculated embeddings

        dot = np.dot(embeddings, self.samples.T)
        abs = np.dot(np.linalg.norm(embeddings, axis=1, keepdims=True), np.linalg.norm(self.samples, axis=1, keepdims=True).T)
        sim = dot / abs
        exp = np.exp(sim)
        sum = np.sum(exp, axis=1, keepdims=True)
        prob = exp / sum
        return prob
    
    def _classify(self, arr: np.ndarray):
        # arr should be have 2 columns. Convert into true or false
        return arr[:, 0] >= arr[:, 1]

    def _construct(self, arr: np.ndarray):
        # Create Pandas series of True or False
        return pd.Series(arr)