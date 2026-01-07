"""add_song_name_to_onboarding

Revision ID: 9920d75a62cc
Revises: 4b5c6d7e8f9a
Create Date: 2026-01-06 22:13:12.777320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9920d75a62cc'
down_revision = '4b5c6d7e8f9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add song_name column
    op.add_column('onboarding_responses', sa.Column('song_name', sa.String(200), nullable=True))
    # Remove upcoming_content column (we removed this field)
    op.drop_column('onboarding_responses', 'upcoming_content')


def downgrade() -> None:
    # Restore upcoming_content column
    op.add_column('onboarding_responses', sa.Column('upcoming_content', sa.Text(), nullable=True))
    # Remove song_name column
    op.drop_column('onboarding_responses', 'song_name')

