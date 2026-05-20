"""initial schema"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.String(64), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("role", sa.String(32), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("resumes", sa.Column("id", sa.String(64), primary_key=True), sa.Column("user_id", sa.String(64), sa.ForeignKey("users.id")), sa.Column("candidate_name", sa.String(255), nullable=False), sa.Column("filename", sa.String(255), nullable=False), sa.Column("raw_text", sa.Text(), nullable=False), sa.Column("parsed", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("analyses", sa.Column("id", sa.String(64), primary_key=True), sa.Column("resume_id", sa.String(64), sa.ForeignKey("resumes.id"), nullable=False), sa.Column("job_description", sa.Text(), nullable=False), sa.Column("ats_score", sa.Float(), nullable=False), sa.Column("semantic_match", sa.Float(), nullable=False), sa.Column("readability_score", sa.Float(), nullable=False), sa.Column("result", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_analyses_resume_id", "analyses", ["resume_id"])
    op.create_table("resume_versions", sa.Column("id", sa.String(64), primary_key=True), sa.Column("resume_id", sa.String(64), sa.ForeignKey("resumes.id"), nullable=False), sa.Column("version_number", sa.Integer(), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("ats_score", sa.Float(), nullable=False), sa.Column("diff", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_resume_versions_resume_id", "resume_versions", ["resume_id"])
    op.create_table("candidates", sa.Column("id", sa.String(64), primary_key=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("role", sa.String(255), nullable=False), sa.Column("match", sa.Float(), nullable=False), sa.Column("ats", sa.Float(), nullable=False), sa.Column("skills", sa.JSON(), nullable=False), sa.Column("risk", sa.String(32), nullable=False))


def downgrade() -> None:
    op.drop_table("candidates")
    op.drop_table("resume_versions")
    op.drop_table("analyses")
    op.drop_table("resumes")
    op.drop_table("users")
