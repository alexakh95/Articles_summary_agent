
from dotenv import load_dotenv
import json,xmltodict
from openai import OpenAI
from pydantic import BaseModel

import os
import trace
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

#lets create a class to extract the data from the pdfs
    
         
class Agent():
    def __init__(self,model, API_KEY, key_words = None, instruction = "", agent_name = ""):
        self.model = model
        self.API_KEY = API_KEY
        self.key_words = key_words
        self.instruction = instruction
        self.agent_name = agent_name
        
    
    def agent_initializing(self):
        
        agent = OpenAI(api_key = self.API_KEY)
        return agent
    
    
    def edit_ptompt(self, path_to_prompt):
        
        try:
            with open(path_to_prompt, 'r') as file:
                    prompt = file.read()
        except KeyError as e:
            print(f"Error reading the file {path_to_prompt}: {e}")
            return
            
        keywords_str = ','.join(self.key_words)
        prompt.replace('{keywords}', keywords_str)
            
        with open(path_to_prompt, 'w') as file:
            file.write(prompt)
            
    def run_agent(self, path_to_prompt):
        """_summary_

        Args:
            path_to_prompt (_type_): path to directory of prompts (prompts are in numerical order)

        Returns:
            txt: The final reponse from the conversation with LLM based on the prompts in the prompt directory 
        """
        #agent initialization
        agent = self.agent_initializing()
        
        #edit the prompt
        self.edit_ptompt(path_to_prompt)
        
        response_id = None
        #creating a conversation with llm based on prompt 
        try: 
            for prompt in os.listdir(path_to_prompt):
                
                    if response_id is not None:
                        response = agent.responses.create(
                            model=self.model,
                            previous_response_id=response_id,
                            file=open(prompt, "rb"),
                            instruction=self.instruction,
                        )
                        response_id = response.id
                    else:
                        response = agent.responses.create(
                            model=self.model,
                            file=open(prompt, "rb"),
                            instruction=self.instruction,
                        )
                        response_id = response.id
        except KeyError as e:
            print(f"Error reading the file {prompt}: {e}")
            return
                
        return response.output[0].content[0].text
    
    def parse_response(self, response):
        """_summary_

        Args:
            response (str): text is the response from LLM with XML tags

        Returns:
            JSON structure: returns the JSON structure of the response 
        """
        return json.dumps(xmltodict.parse(response, indent=4))
        
                             
                

        
        
        


                    

                    

                    
        
        
    
urls = "https://serpapi.com/search"

articles = Article_extraction(urls=urls)

#lets get the data from each web_site save it and then will move using a prompt 
articles.get_data_from_pdf(filename='articles.txt')



       