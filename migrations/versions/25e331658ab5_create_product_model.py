"""Create product model

Revision ID: 25e331658ab5
Revises: e03a61051234
Create Date: 2026-08-01
"""

from alembic import op
import sqlalchemy as sa


revision = '25e331658ab5'
down_revision = 'e03a61051234'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'products',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'name',
            sa.String(length=150),
            nullable=False
        ),

        sa.Column(
            'slug',
            sa.String(length=150),
            nullable=False
        ),

        sa.Column(
            'description',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'price',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'image',
            sa.String(length=255),
            nullable=True
        ),

        sa.Column(
            'featured',
            sa.Boolean(),
            nullable=True
        ),

        sa.Column(
            'service_id',
            sa.Integer(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ['service_id'],
            ['services.id'],
            name='fk_products_service'
        ),

        sa.PrimaryKeyConstraint(
            'id'
        ),

        sa.UniqueConstraint(
            'slug',
            name='uq_products_slug'
        )
    )


def downgrade():

    op.drop_table('products')