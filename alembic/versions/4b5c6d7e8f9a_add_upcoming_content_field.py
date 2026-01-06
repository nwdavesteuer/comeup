"""Add upcoming_content field to onboarding

Revision ID: 4b5c6d7e8f9a
Revises: 3a6545303a8e
Create Date: 2026-01-05 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b5c6d7e8f9a'
down_revision = '3a6545303a8e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('onboarding_responses', sa.Column('upcoming_content', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('onboarding_responses', 'upcoming_content')

