from openai import OpenAI
from src.utils.config import settings
from pydantic import BaseModel, Field
from typing import List, Optional
import json

client = OpenAI(api_key=settings.openai_api_key)

class SkillAssessment(BaseModel):
    skill_name: str = Field(description="Name of the skill")
    proficiency_level: str = Field(description="Beginner/Intermediate/Advanced/Expert")
    years_estimated: int = Field(description="Estimated years to master", ge=0, le=20)
    resources: List[str] = Field(description="Top 3 learning resources")
next_step: str = Field(description="Immediate actionable next step")

class CareerAnalysis(BaseModel):
    candidate_summary: str = Field(description="2-sentence candidate summary")
    top_skills: List[SkillAssessment] = Field(description="Top 3 skills assessed")
    career_trajectory: str = Field(description="Recommended career path")
    salary_range: str = Field(description="Estimated salary range in USD")
    strengths: List[str] = Field(description="Key strengths")
    gaps: List[str] = Field(description="Areas needing improvement")
    immediate_actions: List[str] = Field(description="3 actions to take this week")
    