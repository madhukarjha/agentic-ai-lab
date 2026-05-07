import hashlib
import json
import shelve
import time
from pathlib import Path
from typing import Any

CACHE_DIR = Path.home() / ".cache" / "agentic-ai-lab"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = str(CACHE_DIR / "responses")


def _make_key(model: str, messages: list, **kwargs) -> str:
    payload = json.dumps({"model": model, "messages": messages, **kwargs}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def cached_chat(client, model: str, messages: list, ttl: int = 86400, **kwargs) -> Any:
    """
    Drop-in wrapper around client.chat.completions.create that caches responses to disk.
    ttl: seconds before cache entry expires (default 24 hours). Set to 0 to disable.
    """
    key = _make_key(model, messages, **kwargs)

    with shelve.open(CACHE_PATH) as db:
        if key in db:
            entry = db[key]
            if ttl == 0 or (time.time() - entry["ts"]) < ttl:
                return entry["response"]

    response = client.chat.completions.create(model=model, messages=messages, **kwargs)

    with shelve.open(CACHE_PATH) as db:
        db[key] = {"response": response, "ts": time.time()}

    return response


def cached_parse(client, model: str, messages: list, response_format, ttl: int = 86400, **kwargs) -> Any:
    """
    Drop-in wrapper around client.beta.chat.completions.parse that caches the parsed result.
    Returns the parsed Pydantic model directly (not the full response object).
    """
    key = _make_key(model, messages, response_format=response_format.__name__, **kwargs)

    with shelve.open(CACHE_PATH) as db:
        if key in db:
            entry = db[key]
            if ttl == 0 or (time.time() - entry["ts"]) < ttl:
                return response_format.model_validate(entry["response"])

    response = client.beta.chat.completions.parse(
        model=model, messages=messages, response_format=response_format, **kwargs
    )
    parsed = response.choices[0].message.parsed

    with shelve.open(CACHE_PATH) as db:
        db[key] = {"response": parsed.model_dump(), "ts": time.time()}

    return parsed


def clear_cache() -> None:
    for f in CACHE_DIR.glob("responses*"):
        f.unlink()
    print(f"Cache cleared: {CACHE_DIR}")
