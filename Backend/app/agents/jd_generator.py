import json

from app.core.agent_llm_client import call_with_tool

SYSTEM_PROMPT = """You are the JD Generation Agent inside Hirly, an AI-native \
recruitment operating system (FR-2: AI job description generation). You are \
given a structured job requirements draft (title, experience, required_skills, \
preferred_skills, responsibilities) produced by the Requirement Extraction \
Agent. Write a complete, professional job description from it.

Rules:
- Only describe skills, responsibilities, and requirements that are present in \
the input — do not invent additional requirements, benefits, salary, location, \
or company details that weren't provided.
- Write in clear, welcoming, professional recruiting language — not a dry \
restatement of the input lists.
- "About the Role" should be a short (2-4 sentence) narrative paragraph \
synthesizing the title, experience level, and core responsibilities.
- "Responsibilities" should expand the input responsibilities into natural, \
readable bullet points (rephrase, don't just copy verbatim).
- "Required Qualifications" must cover every item in required_skills plus the \
stated experience requirement.
- "Preferred Qualifications" must cover every item in preferred_skills. If \
preferred_skills is empty, omit this section entirely.
- Output must be valid Markdown with "##" section headers, ready to publish \
as-is on the candidate portal — this is a human-editable draft the recruiter \
approves or edits before publishing (FR-2), so it should read as finished copy, \
not a placeholder.
"""

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "jd_markdown": {
            "type": "string",
            "description": (
                "The complete job description as Markdown, starting with "
                "'# <Title>' followed by '## About the Role', "
                "'## Responsibilities', '## Required Qualifications', and "
                "(if there are preferred skills) '## Preferred Qualifications'."
            ),
        },
    },
    "required": ["jd_markdown"],
}


def generate_jd(requirements: dict) -> str:
    """
    JD Generation Agent (FR-2).

    Turns the structured requirements draft from the Requirement Extraction
    Agent into a publish-ready Markdown job description via an LLM tool call.
    Returns a plain string (jd_text), matching the previous stub's contract,
    so app/api/routes/jobs.py doesn't have to change.
    """
    response = call_with_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=json.dumps(requirements, indent=2),
        tool_name="write_job_description",
        tool_description="Record the generated job description as Markdown.",
        input_schema=INPUT_SCHEMA,
        max_tokens=2000,
    )

    result = response["result"]
    jd_markdown = result["jd_markdown"].strip()

    # Guard: never hand routes an empty JD if the model somehow returns blank text.
    if not jd_markdown:
        title = requirements.get("title", "Untitled Role")
        jd_markdown = f"# {title}\n\n## About the Role\n(JD generation returned empty — please edit before publishing.)\n"

    return jd_markdown
