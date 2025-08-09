"""
Class: Google
Author: Zain Nomani
Purpose: Run a google search and scrape results, including HTML and corresponding links for each search
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, List
class Google:
    """
    Variables:
        - searchTerms: Defined in initialisation - what to search
        - url: Constructed URL given search terms
        - status: Response Status (200, 404, etc)
        - response: Raw HTML response
        - results: list of HTML google search results
        - links: corresponding links found in each result
    
    Public Methods:
        - search(): Search
        - summarise(): Show results of query

    Constructor Methods:
        _construct(): Given search terms, create a URL. Modify to add extra search parameters as needed
        _search(): Send request to get HTML of search page
        _getResults: Store HTML of each result
        _getURLs: Store links within each HTML result
    """

    def __init__(self, search: str):
        self.searchTerms: str = search
        self.url: Optional[str] = None
        self.status: Optional[int] = None
        self.response: Optional[str] = None
        self.results: Optional[List[str]] = None
        self.links: Optional[List[str]] = None

    def Links(self):
        return self.links


    # Public Methods
    def search(self, num: int = 10) -> "Google":
        self._construct(nums=num)._search()._getResults()._getURLs()
        return self
    
    def summarise(self) -> None:
        print("Search: ", self.searchTerms)
        print("URL Queried: ", self.url)
        print("Status Code: ", self.status)
        print("URLs scraped: ", self.links)
        return None

    # Constructors
    def _construct(self, nums: int = 10) -> "Google":
        """
        Wrap around urlRequest by constructing url
        Requires modification depending on context eg restricting site, search terms, etc
        """
        if self.searchTerms is None:
            raise ValueError("self.searchTerms is not defined")
        search = self.searchTerms.replace(" ", "+")
        search = search.replace(":", "%3A")
        search = search.replace("/", r"%2F")
        url = "https://www.google.com/search?q=" + search + "+site%3Alinkedin.com%2Fin&num=" + str(nums)
        self.url = url
        return self
    
    def _search(self) -> "Google":
        if self.url is None:
            raise ValueError("self.url is not defined")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        url = self.url
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self.status = response.status_code
        self.response = response.text
        return self

    def _getResults(self) -> "Google":
        if self.response is None:
            raise ValueError("self.response is not defined")
        soup = BeautifulSoup(self.response, 'html.parser')
        results = soup.select("div.g")
        self.results = results
        return self

    def _getURLs(self) -> "Google":
        if self.results is None:
            raise ValueError("self.results is not defined")
        urls: list[str] = []
        for result in self.results:
            links = result.find_all("a", href=True)
            url_list = [link['href'] for link in links if link.get('href')]
            url_list = list(set(url_list))
            urls.append(url_list)
        self.links = urls
        return self