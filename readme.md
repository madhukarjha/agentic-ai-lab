uv pip install <package name>
uv pip freeze > requirements.txt

Working command
Inside the repo/venv:

Or with uv if it uses the active venv:
uv run agentic-ai-lab

Also works
python -m src.agents.basic_openai_agent

### Run the basic OpenAI agent:
uv run python src/agents/basic_openai_agent.py
uv run python apps/chatbot.py
uv run python 1-basic.py
uv run python <path/to/any/python/file.py>

### Alternative with pip (if preferred):
Install in editable mode: pip install -e .
Run the predefined script: agentic-ai-lab
Or run modules: python -m src.agents.basic_openai_agent
