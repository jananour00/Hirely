import json

from app.core.agent_llm_client import call_with_tool

DIMENSIONS = [
    "required_skills",
    "experience",
    "technical_evidence",
    "responsibilities_fit",
    "education",
    "soft_skills",
]

SYSTEM_PROMPT = """You are the ATS Matching Agent inside Hirly, an AI-native \
recruitment operating system (FR-6: Semantic ATS Matching & Scoring). You are \
given a job's structured requirements and a candidate's structured profile \
(both already extracted by upstream agents). Score how well the candidate \
matches the role using semantic judgment — not keyword matching. A candidate \
who describes equivalent experience in different words (e.g. "built REST \
services with Django" against a requirement for "backend API development") \
should score as a match.

Score these six dimensions, each from 0.0 (no match) to 1.0 (excellent match):
- required_skills: coverage of the job's required_skills by the candidate's \
skills/experience/projects (semantic, not string match).
- experience: does the candidate's years/seniority/role history line up with \
the job's stated experience requirement?
- technical_evidence: is there concrete evidence (projects, described work) \
backing up claimed skills, vs. skills listed with no substantiation?
- responsibilities_fit: how well the candidate's actual experience/projects \
map onto the job's responsibilities list.
- education: relevance of the candidate's education to the role (do not \
penalize missing formal education if strong practical evidence compensates).
- soft_skills: evidence of collaboration, communication, leadership, etc., \
drawn only from what's actually described (e.g. "led a team of 4", "presented \
to stakeholders") — do not invent soft skills from silence.

Rules:
- Every dimension score MUST come with a one-sentence, human-readable evidence \
string that cites something concrete from the requirements/profile (NFR: \
Explainability). Never return a bare score with generic filler text.
- If a dimension has no supporting evidence either way, score it low-to-mid \
(around 0.3-0.5) and say so plainly in the evidence sentence — don't guess high.
- strengths: 2-5 short bullet points on where this candidate clearly fits.
- gaps: 2-5 short bullet points on where this candidate falls short or is unclear.
- Be calibrated and consistent — same profile/requirements pair should score \
similarly. Do not inflate scores to be encouraging.
"""

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "dimension_scores": {
            "type": "object",
            "description": "One entry per required dimension.",
            "properties": {
                dim: {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": f"Match score for {dim.replace('_', ' ')}, 0.0-1.0.",
                        },
                        "evidence": {
                            "type": "string",
                            "description": "One human-readable sentence justifying the score, citing specifics.",
                        },
                    },
                    "required": ["score", "evidence"],
                }
                for dim in DIMENSIONS
            },
            "required": DIMENSIONS,
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"},
            "description": "2-5 short bullet points on where the candidate fits well.",
        },
        "gaps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "2-5 short bullet points on where the candidate falls short or is unclear.",
        },
    },
    "required": ["dimension_scores", "strengths", "gaps"],
}


def score_candidate(requirements: dict, profile: dict) -> dict:
    """
    ATS Matching Agent (FR-6, FR-7).

    Scores a candidate profile against a job's requirements via an LLM tool
    call, used as a pragmatic stand-in for the SRS's embedding-based semantic
    matcher — same evidence-per-dimension contract (NFR: Explainability), same
    return shape as the previous stub, so nothing downstream (ATSEvaluation
    model, ranking service) has to change.

    overall_score is the mean of the six dimension scores, computed here
    (not by the model) so it's always numerically consistent with the
    per-dimension scores the model returns.
    """
    user_message = (
        "JOB REQUIREMENTS:\n"
        f"{json.dumps(requirements, indent=2)}\n\n"
        "CANDIDATE PROFILE:\n"
        f"{json.dumps(profile, indent=2)}"
    )

    response = call_with_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tool_name="score_candidate_match",
        tool_description="Record the multi-dimension ATS match score for this candidate against this job.",
        input_schema=INPUT_SCHEMA,
        max_tokens=2000,
    )

    result = response["result"]
    dimension_scores = result["dimension_scores"]

    # Guard against a dropped dimension or an out-of-range score from the
    # model — never let a malformed LLM response corrupt the stored evaluation.
    for dim in DIMENSIONS:
        entry = dimension_scores.get(dim) or {"score": 0.5, "evidence": f"No evidence returned for {dim.replace('_', ' ')}."}
        score = entry.get("score", 0.5)
        entry["score"] = max(0.0, min(1.0, float(score)))
        entry.setdefault("evidence", f"No evidence returned for {dim.replace('_', ' ')}.")
        dimension_scores[dim] = entry

    overall_score = sum(dimension_scores[dim]["score"] for dim in DIMENSIONS) / len(DIMENSIONS)

    return {
        "overall_score": overall_score,
        "dimension_scores": dimension_scores,
        "strengths": result.get("strengths") or [],
        "gaps": result.get("gaps") or [],
    }
