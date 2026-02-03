from fastmcp import FastMCP
import datetime

mcp = FastMCP("DateTime MCP")

@mcp.tool
def get_current_date() -> str:
    print("called get_current_date")
    return datetime.date.today().isoformat()

@mcp.tool
def get_current_datetime() -> str:
    print("called get_current_datetime")
    return datetime.datetime.now().isoformat(timespec="seconds")

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)
