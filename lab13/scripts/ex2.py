import json
from openai import OpenAI
import polars as pl
import requests
from io import BytesIO

def read_remote_csv(url: str) -> str:
    data = requests.get(url).content
    df = pl.read_csv(BytesIO(data))
    print("csv called")
    return str(df.head(5).to_dict())

def read_remote_parquet(url: str) -> str:
    data = requests.get(url).content
    df = pl.read_parquet(BytesIO(data))
    print("parqet called")
    return str(df.head(5).to_dict())


client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_remote_csv",
            "description": "Read CSV file from URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_remote_parquet",
            "description": "Read parquet file from URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You analyze datasets."},
    {
        "role": "user",
        "content": (
            "Decribe what you see in this dataset: https://raw.githubusercontent.com/j-adamczyk/ApisTox_dataset/master/outputs/dataset_final.csv"
        )
    }
]

response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

call = response.choices[0].message.tool_calls[0]
name, args = call.function.name, json.loads(call.function.arguments)

print(f"Using tool {name}")
if name == "read_remote_csv":
    result = read_remote_csv(**args)

elif name == "read_remote_parquet":
    result = read_remote_parquet(**args)

else:
    raise NameError()


messages.append(response.choices[0].message)
messages.append({
    "role": "tool", 
    "tool_call_id": call.id, 
    "content": result
})

final_response = client.chat.completions.create(model="qwen2.5:1.5b", messages=messages)
print(final_response.choices[0].message.content)