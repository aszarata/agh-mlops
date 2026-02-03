from fastmcp import FastMCP
from typing import List
import matplotlib.pyplot as plt
from io import BytesIO
import base64

mcp = FastMCP("Plot MCP")

@mcp.tool
def line_plot(
    data: List[float],
    title: str = "",
) -> str:
    try:
        for series in data:
            plt.plot(series)

        if title:
            plt.title(title)

    except Exception:
        print("AAAA")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    return base64.b64encode(buf.getvalue()).decode()

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8003)
