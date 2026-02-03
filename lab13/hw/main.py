import asyncio
import json
from contextlib import AsyncExitStack
from openai import OpenAI
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPManager:
    def __init__(self, servers: dict[str, str]):
        self.servers = servers
        self.clients = {}
        self.tools = []  # in OpenAI format
        self._stack = AsyncExitStack()

    async def __aenter__(self):
        for url in self.servers.values():
            read, write, session_id = await self._stack.enter_async_context(
                streamable_http_client(url)
            )
            session = await self._stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            tools_resp = await session.list_tools()
            for t in tools_resp.tools:
                self.clients[t.name] = session
                self.tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description,
                            "parameters": t.inputSchema,
                        },
                    }
                )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._stack.aclose()

    async def call_tool(self, name: str, args: dict) -> dict | str:
        result = await self.clients[name].call_tool(name, arguments=args)
        return result.content[0].text


async def make_llm_request(prompt: str) -> str:
    mcp_servers = {
        "plot_data_server": "http://localhost:8003/mcp",
        "datetime_server": "http://localhost:8002/mcp",
    }

    vllm_client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

    async with MCPManager(mcp_servers) as mcp:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Use tools if you need to."
                    "When calling tools, provide arguments as proper JSON values, "
                    # "If the task is impossible based on your knowledge and tools, "
                    # "return that information."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        # guard: loop limit, we break as soon as we get an answer
        for _ in range(10):
            response = vllm_client.chat.completions.create(
                model="qwen2.5:1.5b",
                messages=messages,
                tools=mcp.tools,
                tool_choice="auto",
                max_completion_tokens=1000,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            )

            response = response.choices[0].message
            if not response.tool_calls:
                return response.content

            messages.append(response)
            for tool_call in response.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"Executing tool '{func_name}'")
                func_result = await mcp.call_tool(func_name, func_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": str(func_result),
                    }
                )


if __name__ == "__main__":
    response = asyncio.run(make_llm_request())
