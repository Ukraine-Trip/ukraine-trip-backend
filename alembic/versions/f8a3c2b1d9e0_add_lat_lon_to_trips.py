"""add lat lon to trips

Revision ID: f8a3c2b1d9e0
Revises: 54e9d484c399
Create Date: 2026-05-07 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f8a3c2b1d9e0'
down_revision: Union[str, Sequence[str], None] = '54e9d484c399'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('trips', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('trips', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('trips', 'longitude')
    op.drop_column('trips', 'latitude')
