from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

from dotenv import load_dotenv
load_dotenv()


server_params = StdioServerParameters(
    command="python",
    args=["math_server.py"],
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            # By using the Ollama model hosted on local system
            agent = create_react_agent("ollama:qwen3:8b", tools=tools)

            # By using the Groq api key
            # agent = create_react_agent("groq:llama3-8b-8192", tools=tools)
            agent_response = await agent.ainvoke({"messages": "what's (15 + 10) x 8?"})
            print("Agent response:", agent_response)

            # print("Agent response: ", agent_response["messages"][-1]["content"])

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
