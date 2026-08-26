"""
Standalone smoke test for the CV Intelligence Agent.
Doesn't touch the DB or FastAPI app — just calls the agent function directly.

Run from Backend/:
    pip install -r requirements.txt
    python test_cv_parser.py
"""
import json

from app.agents.cv_parser import parse_cv

SAMPLE = """
Jane Doe
jane.doe@email.com | linkedin.com/in/janedoe | github.com/janedoe

EDUCATION
B.Sc. Computer Science, Cairo University, 2019 - 2023

EXPERIENCE
Backend Engineer, Acme Corp (2023 - present)
- Built and maintained REST APIs in Python/FastAPI serving 50k+ daily users
- Migrated legacy PostgreSQL schema with zero downtime

Software Engineering Intern, StartupCo (Summer 2022)
- Shipped a Django dashboard used internally by the ops team

PROJECTS
Recipe Finder - A Flutter app that recommends recipes from pantry ingredients

SKILLS
Python, FastAPI, Django, PostgreSQL, Docker, Git

LANGUAGES
English (fluent), Arabic (native)

CERTIFICATIONS
AWS Certified Cloud Practitioner
"""

if __name__ == "__main__":
    result = parse_cv(SAMPLE)
    print(json.dumps(result, indent=2))
