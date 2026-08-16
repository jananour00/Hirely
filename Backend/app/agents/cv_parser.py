def parse_cv(raw_text: str) -> dict:
    """
    Stub CV Intelligence agent (FR-5 entity extraction).
    Replace with an Anthropic API structured-output call later — keep this
    function's return shape identical so nothing downstream changes.
    """
    return {
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "languages": [],
        "links": [],
        "low_confidence_fields": ["education", "experience", "skills", "projects"],
        "raw_text_preview": raw_text[:500],
    }