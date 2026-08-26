"""
Standalone smoke test for the ATS Matching Agent.
Doesn't touch the DB or FastAPI app — just calls the agent function directly.

Run from Backend/:
    pip install -r requirements.txt
    python test_ats_matcher.py
"""
import json

from app.agents.ats_matcher import score_candidate

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

PROFILE = {
    "education": [{"institution": "Cairo University", "degree": "B.Sc.", "field": "Computer Science"}],
    "experience": [
        {
            "company": "Acme Corp",
            "title": "Backend Engineer",
            "start_date": "2023",
            "end_date": "present",
            "description": "Built and maintained REST APIs in Python/FastAPI serving 50k+ daily users; migrated legacy PostgreSQL schema with zero downtime.",
        }
    ],
    "skills": ["Python", "FastAPI", "Django", "PostgreSQL", "Docker", "Git"],
    "projects": [{"name": "Recipe Finder", "description": "A Flutter app that recommends recipes from pantry ingredients."}],
    "certifications": ["AWS Certified Cloud Practitioner"],
    "languages": ["English", "Arabic"],
    "links": ["github.com/janedoe"],
}

if __name__ == "__main__":
    result = score_candidate(REQUIREMENTS, PROFILE)
    print(json.dumps(result, indent=2))
