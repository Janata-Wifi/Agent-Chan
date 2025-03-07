from utils.browser  import search
from langchain.tools import tool
import json


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
        web_search = search(query)
        
        return web_search
    except Exception as e:
        return f"Error: {e}"




