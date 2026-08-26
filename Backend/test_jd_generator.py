"""
Standalone smoke test for the JD Generation Agent.
Doesn't touch the DB or FastAPI app — just calls the agent function directly.

Run from Backend/:
    pip install -r requirements.txt
    python test_jd_generator.py
"""
from app.agents.jd_generator import generate_jd

REQUIREMENTS = {
    "title": "Senior Backend Engineer",
    "experience": "5+ years",
    "required_skills": ["Python", "PostgreSQL", "FastAPI"],
    "preferred_skills": ["Docker"],
    "responsibilities": [
        "Design our core API",
        "Review PRs from junior engineers",
        "Own our database migrations",
    ],
}

if __name__ == "__main__":
    print(generate_jd(REQUIREMENTS))
