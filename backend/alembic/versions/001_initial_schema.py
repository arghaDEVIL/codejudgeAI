"""Initial schema - create all base tables

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # Create problems table
    op.create_table(
        "problems",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("tags", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("expected_output", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_problems_id"), "problems", ["id"], unique=False)
    op.create_index(op.f("ix_problems_title"), "problems", ["title"], unique=True)
    op.create_index(
        op.f("ix_problems_difficulty"), "problems", ["difficulty"], unique=False
    )

    # Create testcases table
    op.create_table(
        "testcases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=False),
        sa.Column("stdin", sa.Text(), nullable=False),
        sa.Column("expected_output", sa.Text(), nullable=False),
        sa.Column("is_sample", sa.Boolean(), nullable=True, server_default="false"),
        sa.Column("weight", sa.Integer(), nullable=True, server_default="1"),
        sa.Column("time_limit", sa.Integer(), nullable=True, server_default="2000"),
        sa.Column("memory_limit", sa.Integer(), nullable=True, server_default="256"),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_testcases_id"), "testcases", ["id"], unique=False)
    op.create_index(
        op.f("ix_testcases_problem_id"), "testcases", ["problem_id"], unique=False
    )

    # Create submissions table
    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=20), nullable=False),
        sa.Column(
            "status", sa.String(length=50), nullable=True, server_default="Pending"
        ),
        sa.Column("execution_time", sa.Integer(), nullable=True),
        sa.Column("memory_used", sa.Integer(), nullable=True),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_submissions_id"), "submissions", ["id"], unique=False)
    op.create_index(
        op.f("ix_submissions_user_id"), "submissions", ["user_id"], unique=False
    )
    op.create_index(
        op.f("ix_submissions_problem_id"), "submissions", ["problem_id"], unique=False
    )

    # Create testcase_results table
    op.create_table(
        "testcase_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("testcase_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("actual_output", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("execution_time", sa.Integer(), nullable=True),
        sa.Column("memory_used", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["submissions.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["testcase_id"], ["testcases.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_testcase_results_id"), "testcase_results", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_testcase_results_submission_id"),
        "testcase_results",
        ["submission_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_testcase_results_testcase_id"),
        "testcase_results",
        ["testcase_id"],
        unique=False,
    )

    # Create ai_feedback table
    op.create_table(
        "ai_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("overall_feedback", sa.Text(), nullable=False),
        sa.Column("error_analysis", sa.Text(), nullable=True),
        sa.Column("optimization_hints", sa.Text(), nullable=True),
        sa.Column("time_complexity", sa.String(length=50), nullable=True),
        sa.Column("space_complexity", sa.String(length=50), nullable=True),
        sa.Column("code_quality_score", sa.Integer(), nullable=True),
        sa.Column(
            "model_used", sa.String(length=50), nullable=True, server_default="gpt-4"
        ),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["submissions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_feedback_id"), "ai_feedback", ["id"], unique=False)
    op.create_index(
        op.f("ix_ai_feedback_submission_id"),
        "ai_feedback",
        ["submission_id"],
        unique=True,
    )


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_index(op.f("ix_ai_feedback_submission_id"), table_name="ai_feedback")
    op.drop_index(op.f("ix_ai_feedback_id"), table_name="ai_feedback")
    op.drop_table("ai_feedback")

    op.drop_index(
        op.f("ix_testcase_results_testcase_id"), table_name="testcase_results"
    )
    op.drop_index(
        op.f("ix_testcase_results_submission_id"), table_name="testcase_results"
    )
    op.drop_index(op.f("ix_testcase_results_id"), table_name="testcase_results")
    op.drop_table("testcase_results")

    op.drop_index(op.f("ix_submissions_problem_id"), table_name="submissions")
    op.drop_index(op.f("ix_submissions_user_id"), table_name="submissions")
    op.drop_index(op.f("ix_submissions_id"), table_name="submissions")
    op.drop_table("submissions")

    op.drop_index(op.f("ix_testcases_problem_id"), table_name="testcases")
    op.drop_index(op.f("ix_testcases_id"), table_name="testcases")
    op.drop_table("testcases")

    op.drop_index(op.f("ix_problems_difficulty"), table_name="problems")
    op.drop_index(op.f("ix_problems_title"), table_name="problems")
    op.drop_index(op.f("ix_problems_id"), table_name="problems")
    op.drop_table("problems")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
