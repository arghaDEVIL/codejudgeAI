from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, distinct
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

from app.db.database import get_db
from app.models.user import User
from app.models.submission import Submission
from app.models.problem import Problem
from app.core.security import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get comprehensive dashboard statistics for the current user"""

    try:
        user_id = current_user.id

        # Basic submission statistics
        total_submissions = (
            db.query(Submission).filter(Submission.user_id == user_id).count()
        )

        successful_submissions = (
            db.query(Submission)
            .filter(Submission.user_id == user_id, Submission.status == "Accepted")
            .count()
        )

        # Unique solved problems
        solved_problems_count = (
            db.query(distinct(Submission.problem_id))
            .filter(Submission.user_id == user_id, Submission.status == "Accepted")
            .count()
        )

        # Success rate
        success_rate = round(
            (successful_submissions / total_submissions * 100)
            if total_submissions > 0
            else 0,
            1,
        )

        # Favorite language (most used)
        language_stats = (
            db.query(
                Submission.language, func.count(Submission.language).label("count")
            )
            .filter(Submission.user_id == user_id)
            .group_by(Submission.language)
            .order_by(desc("count"))
            .first()
        )

        favorite_language = language_stats.language if language_stats else "Python"

        # Calculate coding streak (consecutive days with submissions)
        streak = calculate_coding_streak(db, user_id)

        # Determine rank based on solved problems
        rank = get_user_rank(solved_problems_count)

        # Recent submissions (last 10)
        recent_submissions = (
            db.query(Submission)
            .filter(Submission.user_id == user_id)
            .order_by(desc(Submission.created_at))
            .limit(10)
            .all()
        )

        # Convert submissions to dict format
        recent_submissions_data = []
        for submission in recent_submissions:
            recent_submissions_data.append(
                {
                    "id": submission.id,
                    "problem_id": submission.problem_id,
                    "language": submission.language,
                    "status": submission.status,
                    "created_at": submission.created_at.isoformat(),
                    "execution_time": submission.execution_time,
                }
            )

        # Language distribution
        language_distribution = (
            db.query(
                Submission.language, func.count(Submission.language).label("count")
            )
            .filter(Submission.user_id == user_id)
            .group_by(Submission.language)
            .all()
        )

        language_stats_data = [
            {"language": lang.language, "count": lang.count}
            for lang in language_distribution
        ]

        # Problem difficulty distribution (for solved problems)
        difficulty_stats = (
            db.query(
                Problem.difficulty,
                func.count(distinct(Submission.problem_id)).label("count"),
            )
            .join(Submission, Problem.id == Submission.problem_id)
            .filter(Submission.user_id == user_id, Submission.status == "Accepted")
            .group_by(Problem.difficulty)
            .all()
        )

        difficulty_distribution = [
            {"difficulty": diff.difficulty, "count": diff.count}
            for diff in difficulty_stats
        ]

        # Calculate total estimated time spent (based on submissions)
        total_time_minutes = (
            total_submissions * 15
        )  # Estimate 15 minutes per submission

        # Weekly activity (submissions per day for last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        weekly_activity = []

        for i in range(7):
            day = seven_days_ago + timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)

            day_submissions = (
                db.query(Submission)
                .filter(
                    Submission.user_id == user_id,
                    Submission.created_at >= day_start,
                    Submission.created_at < day_end,
                )
                .count()
            )

            day_accepted = (
                db.query(Submission)
                .filter(
                    Submission.user_id == user_id,
                    Submission.created_at >= day_start,
                    Submission.created_at < day_end,
                    Submission.status == "Accepted",
                )
                .count()
            )

            day_success_rate = round(
                (day_accepted / day_submissions * 100) if day_submissions > 0 else 0, 1
            )

            weekly_activity.append(
                {
                    "date": day.strftime("%Y-%m-%d"),
                    "submissions": day_submissions,
                    "success_rate": day_success_rate,
                }
            )

        # Generate achievements
        achievements = generate_user_achievements(
            solved_problems_count,
            success_rate,
            streak,
            total_submissions,
            favorite_language,
        )

        return {
            "user": {
                "id": current_user.id,
                "name": current_user.name,
                "email": current_user.email,
                "created_at": current_user.created_at.isoformat()
                if current_user.created_at
                else None,
            },
            "stats": {
                "total_submissions": total_submissions,
                "solved_problems": solved_problems_count,
                "success_rate": success_rate,
                "favorite_language": favorite_language,
                "total_time_minutes": total_time_minutes,
                "streak": streak,
                "rank": rank,
            },
            "recent_submissions": recent_submissions_data,
            "achievements": achievements,
            "analytics": {
                "language_distribution": language_stats_data,
                "difficulty_distribution": difficulty_distribution,
                "weekly_activity": weekly_activity,
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch dashboard stats: {str(e)}"
        )


def calculate_coding_streak(db: Session, user_id: int) -> int:
    """Calculate the current coding streak for a user"""

    # Get submissions from the last 30 days, grouped by date
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    submissions_by_date = (
        db.query(
            func.date(Submission.created_at).label("submission_date"),
            func.count(Submission.id).label("count"),
        )
        .filter(Submission.user_id == user_id, Submission.created_at >= thirty_days_ago)
        .group_by(func.date(Submission.created_at))
        .order_by(desc("submission_date"))
        .all()
    )

    if not submissions_by_date:
        return 0

    # Calculate streak from most recent date backwards
    streak = 0
    current_date = datetime.utcnow().date()

    # Convert to set for faster lookup
    submission_dates = {row.submission_date for row in submissions_by_date}

    # Check if user coded today or yesterday (allow for timezone differences)
    if current_date in submission_dates:
        streak = 1
        check_date = current_date - timedelta(days=1)
    elif (current_date - timedelta(days=1)) in submission_dates:
        streak = 1
        check_date = current_date - timedelta(days=2)
    else:
        return 0

    # Count consecutive days backwards
    while check_date in submission_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return streak


def get_user_rank(solved_problems: int) -> str:
    """Determine user rank based on solved problems"""
    if solved_problems >= 100:
        return "Expert"
    elif solved_problems >= 50:
        return "Advanced"
    elif solved_problems >= 20:
        return "Intermediate"
    elif solved_problems >= 5:
        return "Novice"
    else:
        return "Beginner"


def generate_user_achievements(
    solved_problems: int,
    success_rate: float,
    streak: int,
    total_submissions: int,
    favorite_language: str,
) -> List[Dict[str, Any]]:
    """Generate achievements based on user statistics"""

    achievements = []

    # Problem solving achievements
    if solved_problems >= 1:
        achievements.append(
            {
                "id": "first-solve",
                "title": "First Steps",
                "description": "Solved your first problem",
                "icon": "Trophy",
                "color": "text-yellow-500",
                "earned": True,
                "earned_at": None,  # Could be populated with actual date
            }
        )

    if solved_problems >= 5:
        achievements.append(
            {
                "id": "problem-solver-5",
                "title": "Getting Started",
                "description": "Solved 5 problems",
                "icon": "Target",
                "color": "text-blue-500",
                "earned": True,
            }
        )

    if solved_problems >= 10:
        achievements.append(
            {
                "id": "problem-solver-10",
                "title": "Problem Solver",
                "description": "Solved 10 problems",
                "icon": "Target",
                "color": "text-blue-500",
                "earned": True,
            }
        )

    if solved_problems >= 25:
        achievements.append(
            {
                "id": "problem-solver-25",
                "title": "Rising Star",
                "description": "Solved 25 problems",
                "icon": "Star",
                "color": "text-purple-500",
                "earned": True,
            }
        )

    if solved_problems >= 50:
        achievements.append(
            {
                "id": "coding-master",
                "title": "Coding Master",
                "description": "Solved 50 problems",
                "icon": "Award",
                "color": "text-purple-500",
                "earned": True,
            }
        )

    if solved_problems >= 100:
        achievements.append(
            {
                "id": "century-club",
                "title": "Century Club",
                "description": "Solved 100 problems",
                "icon": "Trophy",
                "color": "text-gold-500",
                "earned": True,
            }
        )

    # Accuracy achievements
    if success_rate >= 70:
        achievements.append(
            {
                "id": "accuracy-good",
                "title": "Accurate Coder",
                "description": "70%+ success rate",
                "icon": "Zap",
                "color": "text-green-500",
                "earned": True,
            }
        )

    if success_rate >= 80:
        achievements.append(
            {
                "id": "accuracy-expert",
                "title": "Accuracy Expert",
                "description": "80%+ success rate",
                "icon": "Zap",
                "color": "text-green-500",
                "earned": True,
            }
        )

    if success_rate >= 90:
        achievements.append(
            {
                "id": "accuracy-master",
                "title": "Precision Master",
                "description": "90%+ success rate",
                "icon": "Zap",
                "color": "text-emerald-500",
                "earned": True,
            }
        )

    # Streak achievements
    if streak >= 3:
        achievements.append(
            {
                "id": "streak-3",
                "title": "Consistent Coder",
                "description": "3-day coding streak",
                "icon": "Activity",
                "color": "text-orange-500",
                "earned": True,
            }
        )

    if streak >= 7:
        achievements.append(
            {
                "id": "week-warrior",
                "title": "Week Warrior",
                "description": "7-day coding streak",
                "icon": "Star",
                "color": "text-orange-500",
                "earned": True,
            }
        )

    if streak >= 30:
        achievements.append(
            {
                "id": "month-master",
                "title": "Month Master",
                "description": "30-day coding streak",
                "icon": "Award",
                "color": "text-red-500",
                "earned": True,
            }
        )

    # Submission volume achievements
    if total_submissions >= 50:
        achievements.append(
            {
                "id": "prolific-coder",
                "title": "Prolific Coder",
                "description": "50+ submissions",
                "icon": "Code",
                "color": "text-indigo-500",
                "earned": True,
            }
        )

    # Language-specific achievements
    if favorite_language == "Python":
        achievements.append(
            {
                "id": "python-lover",
                "title": "Python Enthusiast",
                "description": "Python is your favorite language",
                "icon": "Code2",
                "color": "text-blue-600",
                "earned": True,
            }
        )

    # Add unearned achievements for motivation
    if solved_problems < 100:
        achievements.append(
            {
                "id": "century-club-progress",
                "title": "Century Club",
                "description": "Solve 100 problems",
                "icon": "Trophy",
                "color": "text-gray-400",
                "earned": False,
                "progress": solved_problems,
                "target": 100,
            }
        )

    if success_rate < 90:
        achievements.append(
            {
                "id": "precision-master-progress",
                "title": "Precision Master",
                "description": "Achieve 90%+ success rate",
                "icon": "Zap",
                "color": "text-gray-400",
                "earned": False,
                "progress": success_rate,
                "target": 90,
            }
        )

    return achievements


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get leaderboard data"""

    # Top users by solved problems
    top_users = (
        db.query(
            User.id,
            User.name,
            func.count(distinct(Submission.problem_id)).label("solved_problems"),
            func.count(Submission.id).label("total_submissions"),
        )
        .join(Submission, User.id == Submission.user_id)
        .filter(Submission.status == "Accepted")
        .group_by(User.id, User.name)
        .order_by(desc("solved_problems"))
        .limit(limit)
        .all()
    )

    leaderboard = []
    for i, user in enumerate(top_users, 1):
        leaderboard.append(
            {
                "rank": i,
                "user_id": user.id,
                "name": user.name,
                "solved_problems": user.solved_problems,
                "total_submissions": user.total_submissions,
                "is_current_user": user.id == current_user.id,
            }
        )

    return {"leaderboard": leaderboard}
