import json

from anthropic import Anthropic

from app.core.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)


def call_with_tool(
    system_prompt: str,
    user_message: str,
    tool_name: str,
    tool_description: str,
    input_schema: dict,
    max_tokens: int = 2000,
) -> dict:
    """
    Forces the model to respond via a single tool call, so the output is
    guaranteed structured data matching input_schema — no JSON-parsing gambles.
    Returns the tool's input dict, plus raw usage stats for audit logging.
    """
    response = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
        tools=[{
            "name": tool_name,
            "description": tool_description,
            "input_schema": input_schema,
        }],
        tool_choice={"type": "tool", "name": tool_name},
    )

    tool_use_block = next(b for b in response.content if b.type == "tool_use")

    return {
        "result": tool_use_block.input,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
        "stop_reason": response.stop_reason,
    }


def call_text(system_prompt: str, user_message: str, max_tokens: int = 2000) -> dict:
    """For plain text generation (e.g. the JD itself) — no tool needed."""
    response = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    text_block = next(b for b in response.content if b.type == "text")

    return {
        "result": text_block.text,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
        "stop_reason": response.stop_reason,
    }