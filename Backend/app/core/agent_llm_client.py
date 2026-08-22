"""
Provider-agnostic LLM client for the agents/* modules.

The rest of the codebase (llm_client.py) talks to Anthropic directly.
This module lets the stub agents (requirement_extraction, jd_generator,
cv_parser, ats_matcher) run against Groq or OpenRouter instead, since both
expose an OpenAI-compatible /chat/completions endpoint with tool calling.

Swap providers via LLM_PROVIDER in .env — no code changes needed elsewhere.
"""
import json

from openai import OpenAI

from app.core.config import settings

_PROVIDER_CONFIG = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": lambda: settings.groq_api_key,
        "model": lambda: settings.groq_model,
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": lambda: settings.openrouter_api_key,
        "model": lambda: settings.openrouter_model,
    },
}


def _client_and_model(provider: str | None = None) -> tuple[OpenAI, str]:
    provider = provider or settings.llm_provider
    if provider not in _PROVIDER_CONFIG:
        raise ValueError(f"Unknown LLM provider '{provider}'. Use one of {list(_PROVIDER_CONFIG)}.")
    cfg = _PROVIDER_CONFIG[provider]
    api_key = cfg["api_key"]()
    if not api_key:
        raise RuntimeError(
            f"LLM_PROVIDER is '{provider}' but no API key is set for it in .env "
            f"({provider.upper()}_API_KEY)."
        )
    client = OpenAI(base_url=cfg["base_url"], api_key=api_key)
    return client, cfg["model"]()


def call_with_tool(
    system_prompt: str,
    user_message: str,
    tool_name: str,
    tool_description: str,
    input_schema: dict,
    max_tokens: int = 2000,
    provider: str | None = None,
) -> dict:
    """
    Forces the model to respond via a single tool call, so the output is
    guaranteed structured JSON matching input_schema.

    Mirrors the shape of app/core/llm_client.call_with_tool so agent code
    can switch between the two clients without changing call sites.
    """
    client, model = _client_and_model(provider)

    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": input_schema,
            },
        }],
        tool_choice={"type": "function", "function": {"name": tool_name}},
    )

    message = response.choices[0].message
    tool_call = message.tool_calls[0]
    result = json.loads(tool_call.function.arguments)

    usage = response.usage
    return {
        "result": result,
        "usage": {
            "input_tokens": usage.prompt_tokens if usage else None,
            "output_tokens": usage.completion_tokens if usage else None,
        },
        "stop_reason": response.choices[0].finish_reason,
        "provider": provider or settings.llm_provider,
        "model": model,
    }
