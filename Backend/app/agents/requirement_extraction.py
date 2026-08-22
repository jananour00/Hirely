<<<<<<< HEAD
from app.core.agent_llm_client import call_with_tool

SYSTEM_PROMPT = """You are the Requirement Extraction Agent inside Hirly, an \
AI-native recruitment operating system. A recruiter gives you a short, free-text \
description of a role they want to hire for. Extract a clean, structured job \
requirement draft from it.

Rules:
- Only extract what is stated or clearly implied — do not invent skills, \
seniority, or responsibilities that aren't grounded in the source text.
- If experience isn't mentioned, use "unspecified".
- required_skills: hard requirements (explicitly "must have", or stated plainly \
as needed for the role).
- preferred_skills: anything hedged as "nice to have", "bonus", "plus", or \
otherwise optional.
- responsibilities: concrete day-to-day duties implied by the role, phrased as \
short action statements.
- Keep the title short and human-readable (e.g. "Senior Backend Engineer", not \
a full sentence).
"""

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Short job title."},
        "experience": {
            "type": "string",
            "description": "Required experience, e.g. '5+ years' or 'unspecified'.",
        },
        "required_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Hard/must-have skills.",
        },
        "preferred_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Nice-to-have skills.",
        },
        "responsibilities": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Concrete day-to-day duties.",
        },
    },
    "required": [
        "title",
        "experience",
        "required_skills",
        "preferred_skills",
        "responsibilities",
    ],
}


def extract_requirements(raw_description: str) -> dict:
    """
    Requirement Extraction Agent (FR-1).

    Turns a free-text HR role description into a structured job draft via an
    LLM tool call (see app/core/agent_llm_client.py — provider set by
    LLM_PROVIDER in .env, defaults to Groq).

    Return shape matches the previous stub exactly (plus source_text for
    traceability) so nothing downstream — routes, schemas, JD generator — has
    to change.
    """
    response = call_with_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=raw_description,
        tool_name="extract_job_requirements",
        tool_description="Record the structured job requirements extracted from the recruiter's description.",
        input_schema=INPUT_SCHEMA,
    )

    result = response["result"]
    result["source_text"] = raw_description
    return result
=======
def extract_requirements(raw_description: str) -> dict:
    """
    Stub Requirement Extraction Agent.
    Replace with an Anthropic API call (structured/tool-use output) later —
    keep this function's signature and return shape the same so nothing
    downstream has to change.
    """
    return {
        "title": raw_description.split(",")[0].strip()[:200] or "Untitled Role",
        "experience": "unspecified",
        "required_skills": [],
        "preferred_skills": [],
        "responsibilities": [],
        "source_text": raw_description,
    }
>>>>>>> 11370235c04fdecb3e197487b0bee4d61e3b868a
