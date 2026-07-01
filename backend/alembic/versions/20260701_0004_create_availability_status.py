"""create availability status table

Revision ID: 20260701_0004
Revises: 20260701_0003
Create Date: 2026-07-01 00:00:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260701_0004"
down_revision: str | None = "20260701_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "availability_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_source_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("last_checked", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_changed", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["product_source_id"], ["product_sources.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_source_id", "provider", name="uq_availability_status_source_provider"),
    )
    op.create_index(op.f("ix_availability_status_id"), "availability_status", ["id"], unique=False)
    op.create_index(op.f("ix_availability_status_product_source_id"), "availability_status", ["product_source_id"], unique=False)
    op.create_index(op.f("ix_availability_status_provider"), "availability_status", ["provider"], unique=False)
    op.create_index(op.f("ix_availability_status_status"), "availability_status", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_availability_status_status"), table_name="availability_status")
    op.drop_index(op.f("ix_availability_status_provider"), table_name="availability_status")
    op.drop_index(op.f("ix_availability_status_product_source_id"), table_name="availability_status")
    op.drop_index(op.f("ix_availability_status_id"), table_name="availability_status")
    op.drop_table("availability_status")

