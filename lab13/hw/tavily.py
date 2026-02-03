import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TavilySearch")
TOKEN = os.environ.get("TAVILY_API_KEY")

@mcp.tool()
def search_travel_info(query: str):
    data = {
        "api_key": TOKEN,
        "query": query,
        "search_depth": "advanced",
        "max_results": 5
    }
    
    req = requests.post("https://api.tavily.com/search", json=data)
    req.raise_for_status()
    
    output = []
    for item in req.json().get("results", []):
        output.append(f"Source: {item['url']}\nContent: {item['content']}")
        
    return "\n\n".join(output)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)