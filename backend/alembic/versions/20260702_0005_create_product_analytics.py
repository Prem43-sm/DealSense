"""create product analytics table

Revision ID: 20260702_0005
Revises: 20260701_0004
Create Date: 2026-07-02 00:00:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260702_0005"
down_revision: str | None = "20260701_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "product_analytics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("views", sa.Integer(), server_default="0", nullable=False),
        sa.Column("searches", sa.Integer(), server_default="0", nullable=False),
        sa.Column("affiliate_clicks", sa.Integer(), server_default="0", nullable=False),
        sa.Column("wishlist_adds", sa.Integer(), server_default="0", nullable=False),
        sa.Column("compare_adds", sa.Integer(), server_default="0", nullable=False),
        sa.Column("detail_page_visits", sa.Integer(), server_default="0", nullable=False),
        sa.Column("score", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "date", name="uq_product_analytics_product_date"),
    )
    op.create_index(op.f("ix_product_analytics_id"), "product_analytics", ["id"], unique=False)
    op.create_index(op.f("ix_product_analytics_product_id"), "product_analytics", ["product_id"], unique=False)
    op.create_index(op.f("ix_product_analytics_date"), "product_analytics", ["date"], unique=False)
    op.create_index(op.f("ix_product_analytics_score"), "product_analytics", ["score"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_product_analytics_score"), table_name="product_analytics")
    op.drop_index(op.f("ix_product_analytics_date"), table_name="product_analytics")
    op.drop_index(op.f("ix_product_analytics_product_id"), table_name="product_analytics")
    op.drop_index(op.f("ix_product_analytics_id"), table_name="product_analytics")
    op.drop_table("product_analytics")
