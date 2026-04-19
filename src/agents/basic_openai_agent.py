from openai import OpenAI
from src.utils.config import settings


def main() -> None:
    print(settings.openai_api_key)
    

if __name__ == "__main__":
    main()