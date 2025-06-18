# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
# import asyncio

# from mcp.client.streamable_http import streamablehttp_client
# from langchain_mcp_adapters.tools import load_mcp_tools
# from mcp import ClientSession
# from dotenv import load_dotenv
# load_dotenv()

# client = MultiServerMCPClient(
#     {
#         "math":{
#             "command": "python",
#             "args": [r"C:\Users\ravin\path\to\your\langchain-mcp\mcp-client-server\math_server.py"],
#             "transport": "stdio",
#         },
#         "weather": {
#             "url": "http://localhost:8000/mcp",
#             "transport": "streamable-http",
#         }
#     }
# )



# async def main():
#     # async with streamablehttp_client(client) as (read, write):
#     #     async with ClientSession(read, write) as session:
#     #         await session.initialize()

#             tools = await client.get_tools() 

#             # By using the Ollama model hosted on local system
#             # agent = create_react_agent("ollama:qwen3:8b", tools=tools)

#             # By using the Groq api key
#             agent = create_react_agent("groq:llama3-8b-8192", tools=tools)
#             math_agent_response = await agent.ainvoke({"messages": "what's (15 + 10) x 8?"})
#             weather_response = await agent.ainvoke({"messages": "what is the weather in New york?"})
#             print("Weather response:", weather_response)
#             print("Math Agent response:", math_agent_response)

#             # print("Agent response: ", agent_response["messages"][-1]["content"])

# # Entry point
# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Setup MultiServerMCPClient with math (stdio) and weather (HTTP)
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http",
        }
    }
)

# Async main with timeout + graceful error handling
async def main():
    try:
        print("🔄 Loading tools...")
        tools = await asyncio.wait_for(client.get_tools(), timeout=10)
        print("✅ Tools loaded.")

        agent = create_react_agent("groq:llama3-8b-8192", tools=tools)

        # Send math query
        math_response = await agent.ainvoke("what's (15 + 10) x 8?")
        print("🧮 Math Answer:", math_response.content)

        # Send weather query
        weather_response = await agent.ainvoke("what is the weather in New York?")
        print("🌤️ Weather Answer:", weather_response.content)

    except asyncio.TimeoutError:
        print("❌ Tool loading timed out. Check if your math/weather servers are running.")
    except KeyboardInterrupt:
        print("🛑 Interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
