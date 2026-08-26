from app.core.agent_llm_client import call_with_tool

SYSTEM_PROMPT = """You are the CV Intelligence Agent inside Hirly, an AI-native \
recruitment operating system (FR-5: entity extraction). You are given the raw \
text extracted from a candidate's resume/CV (often messy — PDF/DOCX extraction \
artifacts, inconsistent spacing, no reliable layout). Extract a clean, \
structured candidate profile from it.

Rules:
- Only extract what is stated or clearly implied in the text — never invent \
degrees, employers, dates, or skills that aren't grounded in the source text.
- education: list of objects with "institution", "degree", "field", "start_date" \
(or null), "end_date" (or null, use "present" if ongoing).
- experience: list of objects with "company", "title", "start_date", "end_date" \
("present" if ongoing), "description" (1-2 sentence summary of responsibilities \
actually stated).
- skills: flat list of skill strings (technical and professional), deduplicated, \
as they'd appear on a resume (e.g. "Python", "Project Management").
- projects: list of objects with "name" and "description".
- certifications: list of strings.
- languages: list of strings (spoken/written languages, not programming languages \
— those go in skills).
- links: list of URLs found in the text (portfolio, GitHub, LinkedIn, etc).
- low_confidence_fields: list of field names (from the set above) where the \
extraction is uncertain, ambiguous, or the source text was too sparse/garbled to \
extract reliably. Be honest — if the resume text is empty or unusable for a \
field, flag it rather than guessing.

If the raw text looks broken or empty (e.g. failed OCR, garbled extraction), \
still return the schema shape with empty lists and flag every field in \
low_confidence_fields — never fabricate content to fill gaps.
"""

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "institution": {"type": "string"},
                    "degree": {"type": "string"},
                    "field": {"type": "string"},
                    "start_date": {"type": ["string", "null"]},
                    "end_date": {"type": ["string", "null"]},
                },
                "required": ["institution", "degree", "field"],
            },
        },
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "title": {"type": "string"},
                    "start_date": {"type": ["string", "null"]},
                    "end_date": {"type": ["string", "null"]},
                    "description": {"type": "string"},
                },
                "required": ["company", "title"],
            },
        },
        "skills": {"type": "array", "items": {"type": "string"}},
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["name", "description"],
            },
        },
        "certifications": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "array", "items": {"type": "string"}},
        "links": {"type": "array", "items": {"type": "string"}},
        "low_confidence_fields": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "education", "experience", "skills", "projects",
                    "certifications", "languages", "links",
                ],
            },
        },
    },
    "required": [
        "education", "experience", "skills", "projects",
        "certifications", "languages", "links", "low_confidence_fields",
    ],
}

# Keep the raw text prompt bounded — CVs can run long and this agent only
# needs the textual content, not every page of a multi-doc portfolio.
_MAX_INPUT_CHARS = 12000


def parse_cv(raw_text: str) -> dict:
    """
    CV Intelligence Agent (FR-5 entity extraction).

    Turns raw resume text (already OCR'd/extracted upstream by
    app/core/text_extraction.py) into a structured candidate profile via an
    LLM tool call (see app/core/agent_llm_client.py).

    Return shape matches the previous stub exactly (plus raw_text_preview)
    so nothing downstream — orchestrator, CandidateProfile model — has to change.
    """
    truncated = raw_text[:_MAX_INPUT_CHARS]

    response = call_with_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=truncated,
        tool_name="extract_candidate_profile",
        tool_description="Record the structured candidate profile extracted from the resume text.",
        input_schema=INPUT_SCHEMA,
        max_tokens=3000,
    )

    result = response["result"]
    result["raw_text_preview"] = raw_text[:500]
    return result
