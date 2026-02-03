import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherPlanner")
KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherService:
    @staticmethod
    def locate(name):
        res = requests.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={"q": name, "limit": 1, "appid": KEY}
        ).json()
        return (res[0]["lat"], res[0]["lon"]) if res else (None, None)

@mcp.tool()
def get_daily_forecast(city: str, days: int = 7):
    y, x = WeatherService.locate(city)
    if y is None:
        return f"Error: City '{city}' not found."
    
    endpoint = "https://api.openweathermap.org/data/2.5/forecast/daily"
    payload = {"lat": y, "lon": x, "cnt": days, "appid": KEY}
    return requests.get(endpoint, params=payload).json()

@mcp.tool()
def get_monthly_averages(city: str):
    y, x = WeatherService.locate(city)
    if y is None:
        return f"Error: City '{city}' not found."

    target = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={y}&lon={x}&appid={KEY}"
    return requests.get(target).json()

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8003)