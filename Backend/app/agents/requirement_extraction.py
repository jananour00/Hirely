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