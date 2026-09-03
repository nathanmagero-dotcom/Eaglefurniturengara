"""Add product subcategories

Revision ID: ad141f5bf3be
Revises: 477fa834734a
Create Date: 2026-08-28 19:42:15.756578

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ad141f5bf3be"
down_revision = "477fa834734a"
branch_labels = None
depends_on = None


def upgrade():

    # ----------------------------------------------------------
    # The subcategories table was already created successfully
    # during the first attempt at this migration.
    #
    # Therefore we DO NOT create it again here.
    # ----------------------------------------------------------

    # Add subcategory reference to products
    with op.batch_alter_table("products", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "subcategory_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_index(
            "ix_products_subcategory_id",
            ["subcategory_id"],
            unique=False
        )

        batch_op.create_foreign_key(
            "fk_products_subcategory",
            "subcategories",
            ["subcategory_id"],
            ["id"]
        )


def downgrade():

    # Remove product → subcategory relationship
    with op.batch_alter_table("products", schema=None) as batch_op:

        batch_op.drop_constraint(
            "fk_products_subcategory",
            type_="foreignkey"
        )

        batch_op.drop_index(
            "ix_products_subcategory_id"
        )

        batch_op.drop_column(
            "subcategory_id"
        )

    # Remove subcategories table
    op.drop_table("subcategories")