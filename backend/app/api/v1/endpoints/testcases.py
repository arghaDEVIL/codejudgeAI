from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.testcase import Testcase
from app.models.problem import Problem
from app.models.user import User
from app.schemas.testcase import TestcaseCreate, TestcaseResponse, TestcasePublic
from app.core.security import get_current_user, get_admin_user

router = APIRouter()


@router.post("/", response_model=TestcaseResponse, status_code=status.HTTP_201_CREATED)
def create_testcase(
    testcase_data: TestcaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),  # Admin only
):
    """Create a new testcase for a problem (admin only)"""

    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == testcase_data.problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    # Create testcase
    testcase = Testcase(
        problem_id=testcase_data.problem_id,
        stdin=testcase_data.stdin,
        expected_output=testcase_data.expected_output,
        is_sample=testcase_data.is_sample,
        weight=testcase_data.weight,
        time_limit=testcase_data.time_limit,
        memory_limit=testcase_data.memory_limit,
        description=testcase_data.description,
    )

    db.add(testcase)
    db.commit()
    db.refresh(testcase)

    return testcase


@router.get("/problem/{problem_id}", response_model=List[TestcasePublic])
def get_problem_testcases(problem_id: int, db: Session = Depends(get_db)):
    """
    Get testcases for a problem
    Returns only sample testcases with full details
    Hidden testcases shown without stdin/expected_output
    """

    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    testcases = db.query(Testcase).filter(Testcase.problem_id == problem_id).all()

    # Return public view
    public_testcases = []
    for tc in testcases:
        public_tc = TestcasePublic(
            id=tc.id,
            is_sample=tc.is_sample,
            description=tc.description,
            stdin=tc.stdin if tc.is_sample else None,
            expected_output=tc.expected_output if tc.is_sample else None,
        )
        public_testcases.append(public_tc)

    return public_testcases


@router.get("/{testcase_id}", response_model=TestcaseResponse)
def get_testcase(
    testcase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),  # Admin only
):
    """Get a specific testcase with full details (admin only)"""

    testcase = db.query(Testcase).filter(Testcase.id == testcase_id).first()

    if not testcase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Testcase not found"
        )

    return testcase


@router.get("/admin/problem/{problem_id}", response_model=List[TestcaseResponse])
def get_all_testcases_admin(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),  # Admin only
):
    """
    Get ALL testcases for a problem with full details (admin only)
    Shows both sample and hidden testcases with complete data
    """

    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    testcases = (
        db.query(Testcase)
        .filter(Testcase.problem_id == problem_id)
        .order_by(Testcase.id)
        .all()
    )
    return testcases


@router.put("/{testcase_id}", response_model=TestcaseResponse)
def update_testcase(
    testcase_id: int,
    testcase_data: TestcaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),  # Admin only
):
    """Update a testcase (admin only)"""

    testcase = db.query(Testcase).filter(Testcase.id == testcase_id).first()

    if not testcase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Testcase not found"
        )

    # Update fields
    testcase.stdin = testcase_data.stdin
    testcase.expected_output = testcase_data.expected_output
    testcase.is_sample = testcase_data.is_sample
    testcase.weight = testcase_data.weight
    testcase.time_limit = testcase_data.time_limit
    testcase.memory_limit = testcase_data.memory_limit
    testcase.description = testcase_data.description

    db.commit()
    db.refresh(testcase)

    return testcase


@router.delete("/{testcase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testcase(
    testcase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),  # Admin only
):
    """Delete a testcase (admin only)"""

    testcase = db.query(Testcase).filter(Testcase.id == testcase_id).first()

    if not testcase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Testcase not found"
        )

    db.delete(testcase)
    db.commit()

    return None
