"""empty message

Revision ID: ec40e28668b4
Revises: 9dc2109395fe
Create Date: 2020-01-21 19:56:28.704533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec40e28668b4'
down_revision = '9dc2109395fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'score')
    op.add_column('users', sa.Column('score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'score')
    op.add_column('roles', sa.Column('score', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###