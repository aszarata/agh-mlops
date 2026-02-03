import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherPlanner")
API = os.getenv("OPENWEATHER_API_KEY")

def locate(name):
    res = requests.get(
        "http://api.openweathermap.org/geo/1.0/direct",
        params={"q": name, "limit": 1, "appid": API}
    ).json()
    return (res[0]["lat"], res[0]["lon"]) if res else (None, None)

@mcp.tool()
def get_daily_forecast(city: str, days: int = 7):
    y, x = locate(city)
    if y is None:
        return f"City '{city}' not found."
    
    endpoint = "https://api.openweathermap.org/data/2.5/forecast/daily"
    payload = {"lat": y, "lon": x, "cnt": days, "appid": API}
    return requests.get(endpoint, params=payload).json()

@mcp.tool()
def get_monthly_averages(city: str):
    y, x = locate(city)
    if y is None:
        return f"City '{city}' not found."

    target = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={y}&lon={x}&appid={API}"
    return requests.get(target).json()

if __name__ == "__main__":
    mcp.run()