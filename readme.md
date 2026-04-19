uv pip install <package name>
uv pip freeze > requirements.txt

Working command
Inside the repo/venv:

Or with uv if it uses the active venv:
uv run agentic-ai-lab

Also works
python -m src.agents.basic_openai_agent
