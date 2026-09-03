"""Add product storefront fields

Revision ID: 477fa834734a
Revises: 561d54617642
Create Date: 2026-08-25 23:50:03.514426

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "477fa834734a"
down_revision = "561d54617642"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table(
        "products",
        schema=None,
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "sale_price",
                sa.Float(),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "best_seller",
                sa.Boolean(),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "new_arrival",
                sa.Boolean(),
                nullable=True,
            )
        )


def downgrade():

    with op.batch_alter_table(
        "products",
        schema=None,
    ) as batch_op:

        batch_op.drop_column(
            "new_arrival"
        )

        batch_op.drop_column(
            "best_seller"
        )

        batch_op.drop_column(
            "sale_price"
        )