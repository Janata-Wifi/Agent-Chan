import asyncio
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContext
from pydantic import SecretStr, BaseModel
import os
from pydantic import BaseModel
from dotenv import load_dotenv  
load_dotenv() 
    



class browser_use:
    

    def __init__(self,save_history : bool = False):
        self.api_key = SecretStr(os.getenv("GEMINI_API_KEY"))
        self.model = os.getenv("MODEL")
        self.username = os.getenv("USERNAME")
        self.x_password = os.getenv("X_PASSWORD")
        self.chrome_instance_path = os.getenv("CHROME_INSTANCE_PATH")
        self.sensitive_data = {'username': self.username, 'x_password': self.x_password}
        self.save_history = save_history

        llm_params = {
            "api_key": self.api_key,
            "model": self.model,
            
        }
        

        if os.getenv("SAVE_HISTORY_ENABLED"): # Check if SAVE_HISTORY_ENABLED env variable is set
            llm_params["save_history"] = True
            llm_params["save_conversation_path"] = './logs/conversation.json'
        elif self.save_history:
            llm_params["save_history"] = True
            llm_params["save_conversation_path"] = './logs/conversation.json'

        self.llm = ChatGoogleGenerativeAI(**llm_params)
        self.browser_config = BrowserConfig(
            
            chrome_instance_path=self.chrome_instance_path)
        self.browser = Browser(self.browser_config)
        

    def execute_task(self,task,username=None,password=None):
        if username and password is not None:
            self.sensitive_data = {'username': username, 'x_password': password}        
            self.agent = Agent(
            task=task,
            llm=self.llm,
            browser=self.browser,
            sensitive_data=self.sensitive_data,
            
            )
        else:
            self.agent = Agent(
            task=task,
            llm=self.llm,
            browser=self.browser,
            )
      

        history= asyncio.run(self.agent.run(max_steps=400))
        
        history.final_result()  
        print("output\n",history.final_result())   
        #await self.browser.close() # Removed to reuse browser instance
        return history.final_result()

if __name__ == "__main__":
    task = "What is the capital of France? give me answer in json format"
    browser_use = browser_use()
    asyncio.run(browser_use.execute_task(task))