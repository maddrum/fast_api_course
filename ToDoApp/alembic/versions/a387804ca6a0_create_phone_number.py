"""create phone number

Revision ID: a387804ca6a0
Revises: 
Create Date: 2022-06-11 14:52:30.255361

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a387804ca6a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
