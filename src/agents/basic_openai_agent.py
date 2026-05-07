from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from src.utils.config import settings
from src.utils.cache import cached_chat

client= OpenAI(api_key= settings.openai_api_key)

def sample_agent(user_message: str, system_prompt: str = None)-> str:
    messages = [];

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})
    response = cached_chat(
        client,
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

def main() -> None:
    print(settings.openai_api_key)
    result = sample_agent(user_message="Explain what machine learning is.", system_prompt="You are a concise technical expert. Use bullet points. Max 5 points.")
    console = Console()
    console.print(Markdown(result))
     

if __name__ == "__main__":
    main()