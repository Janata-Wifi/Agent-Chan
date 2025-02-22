from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import Tool, tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import os
import json
from dotenv import load_dotenv
import tools.general_data_collect_and_execution
import tools.librenms_access
from tools.general_data_collect_and_execution import traceroute, read_data_from_any_device
from tools.web_search import web_search
from tools.librenms_access import fetch_alerts, fetch_logs

load_dotenv()   
api_key =  os.getenv("GEMINI_API_KEY")

tools_lists = [traceroute, read_data_from_any_device, fetch_alerts, fetch_logs,web_search]
tools = tools_lists
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,  
    api_key=api_key,    
)   

# ReAct Prompt Template (String-based for easier formatting)
react_prompt_template = """Answer the following questions as best as you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: **IMPORTANT! You MUST provide all argument in  JSON format**


Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(react_prompt_template)


agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


result = agent_executor.invoke({
    "input": """
    

"""
})

#print("Raw Agent Output:", result)
print(StrOutputParser().parse(result))

