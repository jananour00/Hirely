DIMENSIONS = [
    "required_skills",
    "experience",
    "technical_evidence",
    "responsibilities_fit",
    "education",
    "soft_skills",
]


def score_candidate(requirements: dict, profile: dict) -> dict:
    """
    Stub ATS Matching Agent (FR-6).
    Replace with real embedding-based semantic matching later — keep this
    function's return shape identical so nothing downstream changes.

    Every dimension MUST ship with an evidence sentence (NFR: Explainability) —
    the stub already enforces that shape so the real agent can't accidentally drop it.
    """
    dimension_scores = {
        dim: {
            "score": 0.5,
            "evidence": f"Stub evidence for {dim.replace('_', ' ')} — real scoring not yet implemented.",
        }
        for dim in DIMENSIONS
    }

    overall_score = sum(d["score"] for d in dimension_scores.values()) / len(dimension_scores)

    return {
        "overall_score": overall_score,
        "dimension_scores": dimension_scores,
        "strengths": ["Stub: no strengths identified yet — real agent pending."],
        "gaps": ["Stub: no gaps identified yet — real agent pending."],
    }