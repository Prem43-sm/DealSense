"""create affiliate links table

Revision ID: 20260701_0003
Revises: 20260701_0002
Create Date: 2026-07-01 00:00:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260701_0003"
down_revision: str | None = "20260701_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "affiliate_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_source_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=120), nullable=False),
        sa.Column("affiliate_url", sa.Text(), nullable=False),
        sa.Column("short_url", sa.Text(), nullable=True),
        sa.Column("tracking_id", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("last_generated", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_checked", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_valid", sa.DateTime(timezone=True), nullable=True),
        sa.Column("click_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["product_source_id"], ["product_sources.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_source_id", "provider", name="uq_affiliate_links_source_provider"),
    )
    op.create_index(op.f("ix_affiliate_links_id"), "affiliate_links", ["id"], unique=False)
    op.create_index(op.f("ix_affiliate_links_product_source_id"), "affiliate_links", ["product_source_id"], unique=False)
    op.create_index(op.f("ix_affiliate_links_provider"), "affiliate_links", ["provider"], unique=False)
    op.create_index(op.f("ix_affiliate_links_status"), "affiliate_links", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_affiliate_links_status"), table_name="affiliate_links")
    op.drop_index(op.f("ix_affiliate_links_provider"), table_name="affiliate_links")
    op.drop_index(op.f("ix_affiliate_links_product_source_id"), table_name="affiliate_links")
    op.drop_index(op.f("ix_affiliate_links_id"), table_name="affiliate_links")
    op.drop_table("affiliate_links")

