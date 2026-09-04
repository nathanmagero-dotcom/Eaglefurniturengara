"""Create missing subcategories table

Revision ID: 8c8b03ee4972
Revises: ad141f5bf3be
"""

from alembic import op
import sqlalchemy as sa


revision = "8c8b03ee4972"
down_revision = "ad141f5bf3be"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "subcategories" not in inspector.get_table_names():

        op.create_table(
            "subcategories",

            sa.Column(
                "id",
                sa.Integer(),
                primary_key=True
            ),

            sa.Column(
                "category_id",
                sa.Integer(),
                sa.ForeignKey("categories.id"),
                nullable=False
            ),

            sa.Column(
                "name",
                sa.String(100),
                nullable=False
            ),

            sa.Column(
                "slug",
                sa.String(120),
                nullable=False,
                unique=True
            ),

            sa.Column(
                "description",
                sa.Text(),
                nullable=True
            ),

            sa.Column(
                "icon",
                sa.String(100),
                nullable=True
            ),

            sa.Column(
                "image",
                sa.String(255),
                nullable=True
            ),

            sa.Column(
                "active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            ),

            sa.Column(
                "display_order",
                sa.Integer(),
                nullable=False,
                server_default="0"
            )
        )

        op.create_index(
            "ix_subcategories_category_id",
            "subcategories",
            ["category_id"],
            unique=False
        )

        op.create_index(
            "ix_subcategories_slug",
            "subcategories",
            ["slug"],
            unique=True
        )


def downgrade():
    pass