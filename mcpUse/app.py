import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
load_dotenv()

async def main():
    """Run a chat using MCP Agents built-in conversation memory."""
   
    config_file = "browser_mcp.json"

    print("Starting Chat")

    client = MCPClient.from_config_file(config_file=config_file)
    
    llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY"))
    
    agent = MCPAgent(
        llm=llm,
        mcp_client=client,
        max_steps=16,
        memory_enabled=True,
    )

    print("\n==== MCP Chat ===")
    print("Type 'exit' to end the chat")
    print("Type 'clear' to clear the memory")
    print("=================================\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        elif user_input.lower() == "clear":
            agent.clear_conversation_history()
            print("Memory cleared")
        else:
            response = await agent.run(user_input)
            print(f"Agent: {response}")
    
    print("\n==== MCP Chat Ended ===")




