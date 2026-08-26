from pydantic import BaseModel


class CandidateProfileOut(BaseModel):
    id: int
    candidate_id: int
    education: list
    experience: list
    skills: list
    projects: list
    certifications: list
    languages: list
    links: list
    low_confidence_fields: list

    model_config = {"from_attributes": True}