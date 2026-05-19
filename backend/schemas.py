from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ProblemCreate(BaseModel):
    title: str
    statement: str
    difficulty: str
    expected_output: str

class SubmissionCreate(BaseModel):
    user_id: int
    problem_id: int
    code: str
    language: str