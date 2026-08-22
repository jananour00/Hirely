"""
Standalone smoke test for the Requirement Extraction Agent.
Doesn't touch the DB or FastAPI app — just calls the agent function directly.

Run from Backend/:
    pip install -r requirements.txt
    python test_requirement_extraction.py
"""
import json

from app.agents.requirement_extraction import extract_requirements

SAMPLE = (
    "We need a Senior Backend Engineer with 5+ years of experience. "
    "Must have strong Python and PostgreSQL skills, and experience with FastAPI. "
    "Experience with Docker is a big plus. They'll be responsible for designing "
    "our core API, reviewing PRs from junior engineers, and owning our database "
    "migrations."
)

if __name__ == "__main__":
    result = extract_requirements(SAMPLE)
    print(json.dumps(result, indent=2))
