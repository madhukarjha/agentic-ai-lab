from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client  = OpenAI()
def think (goal):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content":"You are a helpful AI agent."},
            {"role": "user", "content": f"Goal: {goal}\nWhat should I do next?"} 
            ]
    )
    return response.choices[0].message.content
goal = "Find top 3 programming languages to learn in 2026"
print(think(goal))