"""Aded language focus are analysis

Revision ID: a0603e356d5a
Revises: ef24bee47402
Create Date: 2025-06-21 16:28:56.987046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a0603e356d5a'
down_revision: Union[str, None] = 'ef24bee47402'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('code_refactorings', sa.Column('focus_areas', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('code_refactorings', sa.Column('analysis_result', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('code_refactorings', 'analysis_result')
    op.drop_column('code_refactorings', 'focus_areas')
    # ### end Alembic commands ###
