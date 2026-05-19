from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional

from app.db.database import get_db
from app.models.problem import Problem
from app.models.user import User
from app.schemas.problem import ProblemCreate, ProblemResponse
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
def create_problem(
    problem_data: ProblemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new problem (protected route)"""

    # Check if problem with same title exists
    existing = db.query(Problem).filter(Problem.title == problem_data.title).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problem with this title already exists",
        )

    # Create new problem
    new_problem = Problem(
        title=problem_data.title,
        statement=problem_data.statement,
        difficulty=problem_data.difficulty,
        tags=problem_data.tags or [],
        expected_output=problem_data.expected_output,
    )

    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)

    return new_problem


@router.get("/", response_model=List[ProblemResponse])
def get_all_problems(
    difficulty: Optional[str] = Query(
        None, description="Filter by difficulty (Easy, Medium, Hard)"
    ),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    search: Optional[str] = Query(None, description="Search in title and statement"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of problems per page"),
    db: Session = Depends(get_db),
):
    """Get all problems with optional filtering and pagination"""

    query = db.query(Problem)

    # Filter by difficulty
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)

    # Filter by tags
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        if tag_list:
            # Check if any of the requested tags exist in the problem's tags
            tag_conditions = []
            for tag in tag_list:
                # Use JSON contains for PostgreSQL or similar logic for other DBs
                tag_conditions.append(Problem.tags.contains([tag]))
            query = query.filter(or_(*tag_conditions))

    # Search in title and statement
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Problem.title.ilike(search_term), Problem.statement.ilike(search_term))
        )

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    problems = query.order_by(Problem.id).offset(offset).limit(limit).all()

    return problems


@router.get("/tags", response_model=List[str])
def get_all_tags(db: Session = Depends(get_db)):
    """Get all unique tags used in problems"""

    problems = db.query(Problem).all()
    all_tags = set()

    for problem in problems:
        if problem.tags:
            all_tags.update(problem.tags)

    return sorted(list(all_tags))


@router.get("/stats")
def get_problem_stats(db: Session = Depends(get_db)):
    """Get problem statistics for filtering UI"""

    total_problems = db.query(Problem).count()

    # Count by difficulty
    easy_count = db.query(Problem).filter(Problem.difficulty == "Easy").count()
    medium_count = db.query(Problem).filter(Problem.difficulty == "Medium").count()
    hard_count = db.query(Problem).filter(Problem.difficulty == "Hard").count()

    # Get all tags with counts
    problems = db.query(Problem).all()
    tag_counts = {}

    for problem in problems:
        if problem.tags:
            for tag in problem.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return {
        "total": total_problems,
        "difficulty_counts": {
            "Easy": easy_count,
            "Medium": medium_count,
            "Hard": hard_count,
        },
        "tag_counts": tag_counts,
    }


@router.get("/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    """Get a specific problem by ID"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    return problem
