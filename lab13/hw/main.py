import asyncio
import os
import sys
from dotenv import load_dotenv
from guardrails import Guard
# from guardrails.hub import RestrictToTopic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from ollama import AsyncClient

load_dotenv()

class TravelAgent:
    def __init__(self):
        self.ollama = AsyncClient(host="http://127.0.0.1:11434")
        self.history = [
            {"role": "system", "content": "Assistant mode: Travel Expert. Focus: Weather & Sights. Reject non-travel queries."}
        ]
        # self.guard = Guard().use(
        #     RestrictToTopic,
        #     valid_topics=["travel", "weather", "tourism", "geography", "hotels", "flights"],
        #     invalid_topics=["small talk"],
        #     on_fail="fix",
        # )

    async def _process_ai_response(self, text):
        try:
            return text #self.guard.validate(text).validated_output
        except:
            return "My expertise is limited to travel planning. Please ask about trips or weather."

    async def start_session(self):
        weather_srv = StdioServerParameters(command="python", args=["weather.py"], env=os.environ.copy())
        tavily_srv = StdioServerParameters(command="python", args=["tavily.py"], env=os.environ.copy())

        async with stdio_client(weather_srv) as weather_transport:
            print("Connected to Weather")
            async with stdio_client(tavily_srv) as tavily_transport:
                print("Connected to Tavily")
                w_session = ClientSession(weather_transport[0], weather_transport[1])
                t_session = ClientSession(tavily_transport[0], tavily_transport[1])

                await w_session.initialize()
                await t_session.initialize()
                
                while True:
                    raw_user_input = await asyncio.to_thread(input, "\n$> ")
                    self.history.append({"role": "user", "content": raw_user_input})

                    response = await self.ollama.chat(
                        model=os.environ.get("MODEL_NAME"),
                        messages=self.history
                    )

                    clean_reply = await self._process_ai_response(response["message"]["content"])
                    
                    print(f"\nAssistant: {clean_reply}")
                    self.history.append({"role": "assistant", "content": clean_reply})

if __name__ == "__main__":
    agent = TravelAgent()
    asyncio.run(agent.start_session())