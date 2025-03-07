from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser,BrowserConfig
from pydantic import SecretStr
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


chrome_instance_path= os.getenv("CHROME_INSTANCE_PATH")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

# Create agent with the model


def web_search(query:str):
    browser=Browser(BrowserConfig(chrome_instance_path=chrome_instance_path))
    agent = Agent(
    task=query,
    llm=llm,
    browser=browser
    )
    loop = asyncio.get_event_loop()
    history=loop.run_until_complete(agent.run())
    return history.final_result()

if __name__ == '__main__':
    #query=query()
    query="what is the capital of france. Output should be in JSON"
    result=web_search(query)
    print(result)

    
