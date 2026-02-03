from guardrails import Guard
from guardrails.hub import RestrictToTopic
from openai import OpenAI

TEXT = "What's the best fish?"

guard = Guard().use(
    RestrictToTopic(valid_topics=["fish", "fishes", "fishing"])
)

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=[
        {"role": "system", "content": "Your are a fishing fanatic. You talk only about fishing and nothing else."},
        {"role": "user", "content": TEXT}
    ]
)

text = response.choices[0].message.content

print(f"PROMPT: {TEXT}")
try:
    guard.validate(text)
    print(text)
except Exception as e:
    print("Blocked by guardrails.")
