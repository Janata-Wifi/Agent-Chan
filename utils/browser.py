from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser,BrowserConfig
from pydantic import SecretStr
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
api_key = SecretStr(os.getenv("GEMINI_API_KEY"))
chrome_instance_path= os.getenv("CHROME_INSTANCE_PATH")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=api_key)

# Create agent with the model


def search(task:str):
    browser=Browser(BrowserConfig(chrome_instance_path=chrome_instance_path))
    agent = Agent(
    task=task,
    llm=llm,
    browser=browser
    )
    loop = asyncio.get_event_loop()
    history=loop.run_until_complete(agent.run())
    return history.final_result()

if __name__ == '__main__':
    
    text="what is the capital of france. Output should be in JSON"
    result=query.search(text)
    
    

    
