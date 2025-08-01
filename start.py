
from bs4 import BeautifulSoup
import os
import requests

SERP_API_KEY = os.getenv("SERP_API_KEY")
class Article_extraction():
    """
    This class facilitates the extraction of articles from various websites, focusing on specific topics based on provided keywords.
    It allows you to search for articles related to particular subjects.
    Args:
        urls (list): A list of URLs to search for articles.
        key_words (list, optional): A list of keywords to filter the articles. Defaults to None.
    
    """
    
    def __init__(self, urls, key_words=None):
        self.urls = urls
        self.key_words = key_words
    
    
    def get_data_google_scolar(self):
        """
        Get's the artickes from google scholar website 

        Returns:
            response object: the response object via this object we could access the data 
        """
        params = {
            "engine": "google_scholar",
            "q": "cybersecutiry AI",
            "api_key": SERP_API_KEY
        }
        
        try:
            response = requests.get(self.urls,params = params)
            return response
        
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error:{err}")
    
        
        
    
urls = "https://serpapi.com/search"

articles = Article_extraction(urls=urls)

response = articles.get_data_google_scolar(urls)
data = response.json()

for result in data.get("organic_results", []):
        print(result.get("title"))
        print(result.get("link"))
        print( )