import utils.brower_use  as browser_use
from langchain.tools import tool
import json
import asyncio

browser_use = browser_use.browser_use()

@tool
def web_search(query: str) -> str:
    """Search the web for information.
    
    Args:
        query: The query to search the web for.
        example: {"query":" go to https://example.com and find me the title of the page"}
    Returns:
        A json containing the search results.
    """
    
    query =json.loads(query)
    query = query["query"]
    try:
        web_search = asyncio.run(browser_use.execute_task(query)) 
        
        return web_search
    except Exception as e:
        return f"Error: {e}"




