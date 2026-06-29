"""create price tracking tables

Revision ID: 20260618_0001
Revises:
Create Date: 2026-06-18 00:00:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260618_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("brand", sa.String(length=120), nullable=True),
        sa.Column("category", sa.String(length=120), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_title"), "products", ["title"], unique=False)
    op.create_index(op.f("ix_products_slug"), "products", ["slug"], unique=False)
    op.create_index(op.f("ix_products_brand"), "products", ["brand"], unique=False)
    op.create_index(op.f("ix_products_category"), "products", ["category"], unique=False)

    op.create_table(
        "stores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_stores_id"), "stores", ["id"], unique=False)
    op.create_index(op.f("ix_stores_name"), "stores", ["name"], unique=False)

    op.create_table(
        "prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=False),
        sa.Column("current_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("availability", sa.Boolean(), nullable=False),
        sa.Column("affiliate_url", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "store_id", name="uq_prices_product_store"),
    )
    op.create_index(op.f("ix_prices_id"), "prices", ["id"], unique=False)
    op.create_index(op.f("ix_prices_product_id"), "prices", ["product_id"], unique=False)
    op.create_index(op.f("ix_prices_store_id"), "prices", ["store_id"], unique=False)

    op.create_table(
        "price_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_price_history_id"), "price_history", ["id"], unique=False)
    op.create_index(op.f("ix_price_history_product_id"), "price_history", ["product_id"], unique=False)
    op.create_index(op.f("ix_price_history_store_id"), "price_history", ["store_id"], unique=False)
    op.create_index(op.f("ix_price_history_created_at"), "price_history", ["created_at"], unique=False)

    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("deal_score", sa.Integer(), nullable=False),
        sa.Column("discount_percent", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deals_id"), "deals", ["id"], unique=False)
    op.create_index(op.f("ix_deals_product_id"), "deals", ["product_id"], unique=False)
    op.create_index(op.f("ix_deals_created_at"), "deals", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_deals_created_at"), table_name="deals")
    op.drop_index(op.f("ix_deals_product_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_id"), table_name="deals")
    op.drop_table("deals")
    op.drop_index(op.f("ix_price_history_created_at"), table_name="price_history")
    op.drop_index(op.f("ix_price_history_store_id"), table_name="price_history")
    op.drop_index(op.f("ix_price_history_product_id"), table_name="price_history")
    op.drop_index(op.f("ix_price_history_id"), table_name="price_history")
    op.drop_table("price_history")
    op.drop_index(op.f("ix_prices_store_id"), table_name="prices")
    op.drop_index(op.f("ix_prices_product_id"), table_name="prices")
    op.drop_index(op.f("ix_prices_id"), table_name="prices")
    op.drop_table("prices")
    op.drop_index(op.f("ix_stores_name"), table_name="stores")
    op.drop_index(op.f("ix_stores_id"), table_name="stores")
    op.drop_table("stores")
    op.drop_index(op.f("ix_products_category"), table_name="products")
    op.drop_index(op.f("ix_products_brand"), table_name="products")
    op.drop_index(op.f("ix_products_slug"), table_name="products")
    op.drop_index(op.f("ix_products_title"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
