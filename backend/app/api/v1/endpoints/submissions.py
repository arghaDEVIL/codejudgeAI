from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response
from sqlalchemy.orm import Session
from typing import List
import math

from app.db.database import get_db
from app.models.submission import Submission
from app.models.problem import Problem
from app.models.user import User
from app.models.testcase import Testcase
from app.models.testcase_result import TestcaseResult
from app.models.ai_feedback import AIFeedback
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
    SubmissionResult,
    SubmissionDetailResponse,
)
from app.core.security import get_current_user
from app.services.code_executor import code_executor
from app.services.ai_feedback_service import ai_feedback_service

router = APIRouter()


def generate_ai_feedback_background(
    submission_id: int,
    code: str,
    language: str,
    problem_title: str,
    problem_statement: str,
    status: str,
    testcase_results: list,
    execution_time: int,
    db_session: Session,
):
    """Background task to generate AI feedback"""
    try:
        # Generate feedback
        feedback_data = ai_feedback_service.generate_feedback(
            code=code,
            language=language,
            problem_title=problem_title,
            problem_statement=problem_statement,
            status=status,
            testcase_results=testcase_results,
            execution_time=execution_time,
        )

        # Store in database
        ai_feedback = AIFeedback(
            submission_id=submission_id,
            overall_feedback=feedback_data["overall_feedback"],
            error_analysis=feedback_data.get("error_analysis"),
            optimization_hints=feedback_data.get("optimization_hints"),
            time_complexity=feedback_data.get("time_complexity"),
            space_complexity=feedback_data.get("space_complexity"),
            code_quality_score=feedback_data.get("code_quality_score"),
        )

        db_session.add(ai_feedback)
        db_session.commit()

    except Exception as e:
        print(f"Error generating AI feedback: {e}")
        db_session.rollback()
    finally:
        db_session.close()


@router.post("/", response_model=SubmissionResult, status_code=status.HTTP_201_CREATED)
def submit_code(
    submission_data: SubmissionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit code for a problem (protected route)
    Runs code against all testcases and returns detailed results
    """

    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == submission_data.problem_id).first()

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found"
        )

    # Get all testcases for the problem
    testcases = (
        db.query(Testcase)
        .filter(Testcase.problem_id == submission_data.problem_id)
        .order_by(Testcase.id)
        .all()
    )

    if not testcases:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No testcases found for this problem",
        )

    # Create submission record
    submission = Submission(
        user_id=current_user.id,
        problem_id=submission_data.problem_id,
        code=submission_data.code,
        language=submission_data.language,
        status="Pending",
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Separate sample and hidden testcases
    sample_testcases = [tc for tc in testcases if tc.is_sample]
    hidden_testcases = [tc for tc in testcases if not tc.is_sample]

    # Execute code against all testcases
    testcase_results = []
    sample_passed = 0
    hidden_passed = 0
    total_time = 0
    max_memory = 0.0
    overall_status = "Accepted"

    # Calculate weighted score
    total_weight = sum(tc.weight for tc in testcases)
    earned_weight = 0

    for testcase in testcases:
        # Execute code
        result = code_executor.execute(
            code=submission_data.code,
            language=submission_data.language,
            stdin=testcase.stdin,
            time_limit=testcase.time_limit,
            memory_limit=testcase.memory_limit,
        )

        # Determine testcase status
        if result["status"] == "Passed":
            # Check if output matches
            if result["output"].strip() == testcase.expected_output.strip():
                tc_status = "Passed"
                if testcase.is_sample:
                    sample_passed += 1
                else:
                    hidden_passed += 1
                earned_weight += testcase.weight  # Add weight for passed testcase
            else:
                tc_status = "Wrong Answer"
                if overall_status == "Accepted":
                    overall_status = "Wrong Answer"
        else:
            tc_status = result["status"]
            if overall_status == "Accepted":
                overall_status = tc_status

        # Track metrics
        if result.get("execution_time"):
            total_time += result["execution_time"]
        if result.get("memory_used", 0) > max_memory:
            max_memory = result["memory_used"]

        # Store testcase result
        tc_result = TestcaseResult(
            submission_id=submission.id,
            testcase_id=testcase.id,
            status=tc_status,
            actual_output=result.get("output"),
            error_message=result.get("error"),
            execution_time=result.get("execution_time"),
            memory_used=result.get("memory_used"),
        )

        db.add(tc_result)

        # Prepare result for response (only sample testcases with full details)
        if testcase.is_sample:
            testcase_results.append(
                {
                    "testcase_id": testcase.id,
                    "description": testcase.description,
                    "status": tc_status,
                    "stdin": testcase.stdin,
                    "expected_output": testcase.expected_output,
                    "actual_output": result.get("output"),
                    "error_message": result.get("error"),
                    "execution_time": result.get("execution_time"),
                    "is_sample": True,
                }
            )

    # Calculate final score (0-100)
    final_score = (earned_weight / total_weight * 100) if total_weight > 0 else 0.0

    # Update submission with final status, metrics, and score
    submission.status = overall_status
    submission.execution_time = total_time
    submission.memory_used = max_memory
    submission.score = round(final_score, 2)

    db.commit()
    db.refresh(submission)

    # Generate AI feedback in background
    background_tasks.add_task(
        generate_ai_feedback_background,
        submission_id=submission.id,
        code=submission_data.code,
        language=submission_data.language,
        problem_title=problem.title,
        problem_statement=problem.statement,
        status=overall_status,
        testcase_results=testcase_results,
        execution_time=total_time,
        db_session=Session(bind=db.get_bind()),
    )

    # Prepare response message
    total_passed = sample_passed + hidden_passed
    message = None
    if overall_status == "Accepted":
        message = (
            f"Congratulations! All testcases passed! Score: {submission.score}/100"
        )
    else:
        message = f"Some testcases failed. Score: {submission.score}/100"

    return SubmissionResult(
        submission_id=submission.id,
        status=overall_status,
        passed_testcases=total_passed,
        total_testcases=len(testcases),
        sample_passed=sample_passed,
        sample_total=len(sample_testcases),
        hidden_passed=hidden_passed,
        hidden_total=len(hidden_testcases),
        score=submission.score,
        max_score=100.0,
        execution_time=total_time,
        memory_used=max_memory,
        sample_results=testcase_results,
        message=message,
    )


@router.get("/", response_model=List[SubmissionResponse])
def get_user_submissions(
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    problem_id: int = None,
    page: int = 1,
    limit: int = 20,
):
    """Get all submissions for current user, optionally filtered by problem with pagination"""

    query = db.query(Submission).filter(Submission.user_id == current_user.id)

    if problem_id:
        query = query.filter(Submission.problem_id == problem_id)

    # Get total count for pagination
    total_count = query.count()
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    # Set pagination headers
    response.headers["X-Total-Count"] = str(total_count)
    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Current-Page"] = str(page)
    response.headers["X-Per-Page"] = str(limit)

    # Apply pagination
    offset = (page - 1) * limit
    submissions = (
        query.order_by(Submission.created_at.desc()).offset(offset).limit(limit).all()
    )

    # Add testcase counts
    result = []
    for sub in submissions:
        # Count passed testcases
        passed = (
            db.query(TestcaseResult)
            .filter(
                TestcaseResult.submission_id == sub.id,
                TestcaseResult.status == "Passed",
            )
            .count()
        )

        total = (
            db.query(TestcaseResult)
            .filter(TestcaseResult.submission_id == sub.id)
            .count()
        )

        sub_dict = {
            "id": sub.id,
            "user_id": sub.user_id,
            "problem_id": sub.problem_id,
            "code": sub.code,
            "language": sub.language,
            "status": sub.status,
            "execution_time": sub.execution_time,
            "memory_used": sub.memory_used,
            "created_at": sub.created_at,
            "passed_testcases": passed,
            "total_testcases": total,
            "score": sub.score,
        }
        result.append(sub_dict)

    return result

    return result


@router.get("/{submission_id}", response_model=SubmissionDetailResponse)
def get_submission_detail(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed submission with all testcase results"""

    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id, Submission.user_id == current_user.id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    # Get testcase results
    tc_results = (
        db.query(TestcaseResult)
        .filter(TestcaseResult.submission_id == submission_id)
        .all()
    )

    # Format results (hide details for hidden testcases)
    formatted_results = []
    for tc_result in tc_results:
        testcase = (
            db.query(Testcase).filter(Testcase.id == tc_result.testcase_id).first()
        )

        result_dict = {
            "testcase_id": tc_result.testcase_id,
            "status": tc_result.status,
            "execution_time": tc_result.execution_time,
            "memory_used": tc_result.memory_used,
            "is_sample": testcase.is_sample if testcase else False,
        }

        # Only show details for sample testcases
        if testcase and testcase.is_sample:
            result_dict.update(
                {
                    "description": testcase.description,
                    "stdin": testcase.stdin,
                    "expected_output": testcase.expected_output,
                    "actual_output": tc_result.actual_output,
                    "error_message": tc_result.error_message,
                }
            )

        formatted_results.append(result_dict)

    # Check if AI feedback exists
    has_feedback = (
        db.query(AIFeedback).filter(AIFeedback.submission_id == submission_id).first()
        is not None
    )

    return SubmissionDetailResponse(
        id=submission.id,
        user_id=submission.user_id,
        problem_id=submission.problem_id,
        code=submission.code,
        language=submission.language,
        status=submission.status,
        execution_time=submission.execution_time,
        memory_used=submission.memory_used,
        created_at=submission.created_at,
        testcase_results=formatted_results,
        has_ai_feedback=has_feedback,
    )
