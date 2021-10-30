from typing import List
from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    email: str
    affiliation: str
    age: int
    introduction: str
    skills: List[str] = []


class ReviewInterview(BaseModel):
    interview_id: str
    comment: str


class InterviewRequests(BaseModel):
    interview_id: str
    user_id: str


class Interview(BaseModel):
    interview_id: str
