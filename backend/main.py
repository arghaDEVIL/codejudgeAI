from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from schemas import UserCreate, UserLogin
from auth import hash_password, verify_password
from models import User, Problem
from schemas import UserCreate, UserLogin, ProblemCreate
from models import User, Problem, Submission
from schemas import UserCreate, UserLogin, ProblemCreate, SubmissionCreate
import subprocess
import tempfile
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "AI Code Judge Backend Running"}

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": db_user.id}

@app.post("/problems")
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    new_problem = Problem(
        title=problem.title,
        statement=problem.statement,
        difficulty=problem.difficulty,
        expected_output=problem.expected_output
    )

    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)

    return {
        "message": "Problem added",
        "id": new_problem.id
    }

@app.get("/problems")
def get_problems(db: Session = Depends(get_db)):
    return db.query(Problem).all()

@app.get("/problems/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    return problem

@app.post("/submit")
def submit_code(data: SubmissionCreate, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == data.problem_id).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    status = "Wrong Answer"
    debug = ""
    output = ""

    try:
        if data.language == "python":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as f:
                f.write(data.code)
                source_file = f.name

            result = subprocess.run(
                ["python", source_file],
                capture_output=True,
                text=True,
                timeout=2
            )

            output = result.stdout.strip()
            debug = result.stderr.strip()

            os.unlink(source_file)

        elif data.language == "cpp":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode="w", encoding="utf-8") as f:
                f.write(data.code)
                source_file = f.name

            exe_file = source_file.replace(".cpp", ".exe")

            compile_result = subprocess.run(
                ["g++", source_file, "-o", exe_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            if compile_result.returncode != 0:
                status = "Compilation Error"
                debug = compile_result.stderr.strip()
            else:
                run_result = subprocess.run(
                    [exe_file],
                    capture_output=True,
                    text=True,
                    timeout=2
                )

                output = run_result.stdout.strip()
                debug = run_result.stderr.strip()

            if os.path.exists(source_file):
                os.unlink(source_file)

            if os.path.exists(exe_file):
                os.unlink(exe_file)

        expected = (problem.expected_output or "").strip()

        if status != "Compilation Error":
            if debug:
                status = "Runtime Error"
            elif output == expected:
                status = "Accepted"
            else:
                status = "Wrong Answer"

    except subprocess.TimeoutExpired:
        status = "Time Limit Exceeded"
        debug = "Execution timed out"

    except Exception as e:
        status = "Runtime Error"
        debug = str(e)

    submission = Submission(
        user_id=data.user_id,
        problem_id=data.problem_id,
        code=data.code,
        language=data.language,
        status=status
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "submission_id": submission.id,
        "status": status,
        "output": output,
        "debug": debug
    }

@app.get("/submissions")
def get_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).all()