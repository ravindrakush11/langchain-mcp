import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from langchain_ollama import ChatOllama

# from mcp.client.streamable_http import streamablehttp_client
# from langchain_mcp_adapters.tools import load_mcp_tools
# from mcp import ClientSession

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))

async def main():
    client = MultiServerMCPClient(
    {
        "math":{
            "command": "python",
            "args": [r"C:\Users\ravin\path\to\your\langchain-mcp\multiple-mcp-servers\math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http",
            }
        }
    )
    tools = await client.get_tools() 

    # By using the Ollama model hosted on local system
    # agent = create_react_agent("ollama:qwen3:8b", tools=tools)
    
    # By using the Groq api key
    model = ChatOllama(model="qwen3:8b")
    # model = ChatGroq(model="llama3-8b-8192")
    agent = create_react_agent(model, tools=tools)
    math_agent_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 10?"}]})
    print("Math Agent response:", math_agent_response['messages'][-1].content)

    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in New york?"}]})
  
    print("Weather response:", weather_response["messages"][-1].content)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
