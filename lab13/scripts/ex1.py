import time
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

prompts = [ # prompts proposed by Deepseek
    "Describe a sunset on a foreign planet.", 
    "List three benefits of daily exercise.", 
    "Explain how a microwave works simply.", 
    "Write a haiku about winter silence.", 
    "What is the capital of Portugal?",
    "Summarize the plot of Romeo and Juliet in one sentence.", 
    "Give me a recipe for a classic grilled cheese sandwich.", 
    "Define the word 'metaphor' with an example.", 
    "Suggest a name for a black and white cat.", 
    "How do you say 'thank you' in Japanese?"
]

start = time.time()

for p in prompts:
    client.chat.completions.create(
        model="deepseek-r1:7b",
        messages=[{"role": "user", "content": p}],
        max_tokens=300
    )

end = time.time()

print(f"Total time: {end - start:.2f} s")
