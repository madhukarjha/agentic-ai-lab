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
    
def analyse_career(bio: str) -> CareerAnalysis:
    """Analyse a career bio and return structured assessment."""
    response = client.beta.chat.completions.parse(model="gpt-4o-mini", messages=[
    {
        "role": "system",
        "content": "You are an expert career coach. Analyse the candidate's background and provide structured, actionable career advice."
    },
    {
        "role": "user",
        "content": f"Analyse this candidate profile:\n\n{bio}"
    }
    ],
    response_format=CareerAnalysis, temperature=0,
    # Pass Pydantic model directly
    )
    return response.choices[0].message.parsed
# Usage
bio = """
I am a 28-year-old software developer with 4 years of experience in Java backend development.
I have built REST APIs, worked with Spring Boot and PostgreSQL. Recently I've been learning 
Python and am interested in AI/ML. I have a CS degree and want to transition into AI engineering.
"""

analysis = analyse_career(bio)
print(f"Summary: {analysis.candidate_summary}")
print(f"Career Path: {analysis.career_trajectory}")
print(f"Salary: {analysis.salary_range}")
print("\nTop Skills:")
for skill in analysis.top_skills:
    print(f"  - {skill.skill_name}: {skill.proficiency_level}")
print("\nImmediate Actions:")
for i, action in enumerate(analysis.immediate_actions, 1):
    print(f"  {i}. {action}")
