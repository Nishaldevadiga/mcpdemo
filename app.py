import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os
from dotenv import load_dotenv



async def run_memory_chat():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    config_file = "browser_mcp.json"

    print('Intializing chat.....')

    #create MCP client and agent with memory enabled
    client=MCPClient.from_config_file(config_file)
    llm=ChatGroq(model="qwen-qwq-32b")


    #create agent with memory enabled = True
    agent=MCPAgent(llm=llm,client=client,max_steps=15,memory_enabled=True)

    print("Interactive MCP chat')")
    print("type 'exit' or 'quit' to end the conversation")
    print("type 'clear' to clear the conversation")


    try:
        while True:
            user_input=input("You: ")


            if user_input.lower() in ['exit','quit']:
                print("Exiting chat....")
                break
            elif user_input.lower() == 'clear':
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            #get response from agent
            print("Assisstant: ",end="",flush=True)


            try:
                response=await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"An error occurred: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())
            
                
