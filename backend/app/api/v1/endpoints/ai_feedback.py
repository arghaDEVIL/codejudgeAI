from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.submission import Submission
from app.models.problem import Problem
from app.models.ai_feedback import AIFeedback
from app.models.testcase_result import TestcaseResult
from app.models.user import User
from app.schemas.ai_feedback import AIFeedbackResponse
from app.core.security import get_current_user
from app.services.ai_feedback_service import ai_feedback_service

router = APIRouter()


@router.get("/submission/{submission_id}", response_model=AIFeedbackResponse)
def get_ai_feedback(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get AI feedback for a submission
    Generates feedback if it doesn't exist yet
    """

    # Verify submission belongs to user
    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id, Submission.user_id == current_user.id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    # Check if feedback already exists
    feedback = (
        db.query(AIFeedback).filter(AIFeedback.submission_id == submission_id).first()
    )

    if feedback:
        return feedback

    # Generate new feedback
    problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()

    # Get testcase results
    tc_results = (
        db.query(TestcaseResult)
        .filter(TestcaseResult.submission_id == submission_id)
        .all()
    )

    # Format testcase results for AI
    testcase_results = []
    for tc_result in tc_results:
        testcase_results.append(
            {
                "status": tc_result.status,
                "error": tc_result.error_message,
                "execution_time": tc_result.execution_time,
            }
        )

    # Generate feedback
    feedback_data = ai_feedback_service.generate_feedback(
        code=submission.code,
        language=submission.language,
        problem_title=problem.title,
        problem_statement=problem.statement,
        status=submission.status,
        testcase_results=testcase_results,
        execution_time=submission.execution_time,
    )

    # Store feedback
    feedback = AIFeedback(
        submission_id=submission_id,
        overall_feedback=feedback_data["overall_feedback"],
        error_analysis=feedback_data.get("error_analysis"),
        optimization_hints=feedback_data.get("optimization_hints"),
        time_complexity=feedback_data.get("time_complexity"),
        space_complexity=feedback_data.get("space_complexity"),
        code_quality_score=feedback_data.get("code_quality_score"),
    )

    try:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
    except Exception as e:
        db.rollback()
        # If duplicate, fetch and return existing feedback
        feedback = (
            db.query(AIFeedback)
            .filter(AIFeedback.submission_id == submission_id)
            .first()
        )
        if feedback:
            return feedback
        # If not duplicate error, re-raise
        raise e

    return feedback


@router.post(
    "/submission/{submission_id}/regenerate", response_model=AIFeedbackResponse
)
def regenerate_ai_feedback(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Regenerate AI feedback for a submission"""

    # Verify submission belongs to user
    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id, Submission.user_id == current_user.id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    # Delete existing feedback
    existing_feedback = (
        db.query(AIFeedback).filter(AIFeedback.submission_id == submission_id).first()
    )

    if existing_feedback:
        db.delete(existing_feedback)
        db.commit()

    # Generate new feedback (reuse get_ai_feedback logic)
    return get_ai_feedback(submission_id, db, current_user)
