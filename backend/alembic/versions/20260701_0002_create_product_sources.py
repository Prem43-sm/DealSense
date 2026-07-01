"""create product sources table

Revision ID: 20260701_0002
Revises: 20260618_0001
Create Date: 2026-07-01 00:00:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260701_0002"
down_revision: str | None = "20260618_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "product_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("source_name", sa.String(length=120), nullable=False),
        sa.Column("external_product_id", sa.String(length=255), nullable=False),
        sa.Column("product_url", sa.Text(), nullable=True),
        sa.Column("canonical_url", sa.Text(), nullable=True),
        sa.Column("last_seen", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_name", "external_product_id", name="uq_product_sources_source_external_id"),
    )
    op.create_index(op.f("ix_product_sources_id"), "product_sources", ["id"], unique=False)
    op.create_index(op.f("ix_product_sources_product_id"), "product_sources", ["product_id"], unique=False)
    op.create_index(op.f("ix_product_sources_source_name"), "product_sources", ["source_name"], unique=False)
    op.create_index(op.f("ix_product_sources_external_product_id"), "product_sources", ["external_product_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_product_sources_external_product_id"), table_name="product_sources")
    op.drop_index(op.f("ix_product_sources_source_name"), table_name="product_sources")
    op.drop_index(op.f("ix_product_sources_product_id"), table_name="product_sources")
    op.drop_index(op.f("ix_product_sources_id"), table_name="product_sources")
    op.drop_table("product_sources")
