
from bs4 import BeautifulSoup
import os
from io import BytesIO
import fitz
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
if SERP_API_KEY is None:
    print("There is no API key")
class Article_extraction():
    """
    This class facilitates the extraction of articles from various websites, focusing on specific topics based on provided keywords.
    It allows you to search for articles related to particular subjects.
    Args:
        urls (list): A list of URLs to search for articles.
        key_words (list, optional): A list of keywords to filter the articles. Defaults to None.
    
    """
    key_words = ["AI cybersecutiry","threat detection AI", "AI security"]
    
    def __init__(self, urls, words_to_search=None):
        self.urls = urls
        # Create an instance-specific copy of the class keywords
        if words_to_search is not None:
            self.key_words.extend(words_to_search)
        
    
    def get_data_google_scolar(self):
        """
        Get's the artickes from google scholar website 

        Returns:
            response object: the response object via this object we could access the data 
        """
        #create query to search 
        query = " OR ".join(self.key_words)
        print(f"Searching query: {query}")
        print(SERP_API_KEY)
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": SERP_API_KEY
        }
        
        try:
            response = requests.get(self.urls,params = params)
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error:{http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"A request error occurred: {req_err}")
        
        return None
    
    def file_of_articles(self,response, filename="articles.txt"):
        """Parses a response object and writes article data to a file.

        This method takes the JSON response from the SerpAPI call, extracts
        the title and link for each organic search result, and appends them
        to the specified file.

        Args:
            response (requests.Response): The HTTP response object from the
                SerpAPI request, which is expected to contain JSON data.
            filename (str, optional): The name of the file to write to.
                Defaults to "articles.txt".

        Side Effects:
            - Creates or appends to the specified file in the current directory.
        """
        # Parse the JSON response
        data = response.json()

        for result in data.get("organic_results", []):
            if "title" in result and "link" in result:
                #save data to the external file 
                
                with open(filename, "a") as file:
                    file.write(result.get("title") + "\n")
                    file.write(result.get("link") + "\n")
                    file.write("\n")
    
    
    def get_data_from_pdf(self,filename='article.txt'):
            #search for pdf in link 
            with open(filename,'r') as file:
                lines = file.readlines()
                for i in range(0,len(lines),2):
                    #het the article title and link 
                    title = lines[i].strip()
                    url = lines[i+1].strip()
                    
                    #connect using silenium to get the article pdf file 
                    driver = webdriver.Chrome()
                    driver.get(url)

                    # Wait for page to load
                    driver.implicitly_wait(5)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    
                    # Find PDF link
                    for link in soup.find_all("a", href=True):
                        if ".pdf" in link["href"]:
                            # 3. Open with PyMuPDF
                            response_pdf = requests.get(url)
                            pdf_file = BytesIO(response_pdf.content)

                            doc = fitz.open(stream=pdf_file, filetype="pdf")
                            all_text = ""
                            for page in doc:
                                all_text += page.get_text()
                            doc.close()
                    
                    
                    #then get data from pdf  and store it in JSON :title , content
                    
        
        
    
urls = "https://serpapi.com/search"

articles = Article_extraction(urls=urls)

#lets get the data from each web_site save it and then will move using a prompt 




       