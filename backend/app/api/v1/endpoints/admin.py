from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.db.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.services.problem_importer import ProblemImporter

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to ensure user is admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


@router.post("/import-problems")
async def import_problems(
    background_tasks: BackgroundTasks,
    source: str = "sample",
    limit: int = 20,
    min_rating: int = 800,
    max_rating: int = 1600,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Import problems from various sources (Admin only)"""

    def run_import():
        importer = ProblemImporter()

        if source == "sample":
            return importer.import_sample_problems()
        elif source == "codeforces":
            return importer.import_from_codeforces(limit, min_rating, max_rating)
        elif source == "all":
            count1 = importer.import_sample_problems()
            count2 = importer.import_from_codeforces(limit, min_rating, max_rating)
            return count1 + count2
        else:
            return 0

    # Run import in background
    background_tasks.add_task(run_import)

    return {
        "message": f"Problem import started from {source}",
        "parameters": {
            "source": source,
            "limit": limit,
            "min_rating": min_rating,
            "max_rating": max_rating,
        },
    }


@router.get("/problem-stats")
async def get_problem_stats(
    current_user: User = Depends(require_admin), db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed problem statistics (Admin only)"""

    importer = ProblemImporter()
    stats = importer.get_import_stats()

    return {"stats": stats, "message": "Problem statistics retrieved successfully"}


@router.get("/system-info")
async def get_system_info(
    current_user: User = Depends(require_admin), db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get system information (Admin only)"""

    from app.models.submission import Submission
    from app.models.problem import Problem

    # Get counts
    total_problems = db.query(Problem).count()
    total_submissions = db.query(Submission).count()
    total_users = db.query(User).count()

    # Get recent activity
    recent_submissions = (
        db.query(Submission).order_by(Submission.created_at.desc()).limit(5).all()
    )

    return {
        "system_stats": {
            "total_problems": total_problems,
            "total_submissions": total_submissions,
            "total_users": total_users,
        },
        "recent_activity": [
            {
                "id": sub.id,
                "user_id": sub.user_id,
                "problem_id": sub.problem_id,
                "status": sub.status,
                "created_at": sub.created_at.isoformat() if sub.created_at else None,
            }
            for sub in recent_submissions
        ],
    }
