"""empty message

Revision ID: f03d57a4d9c0
Revises: 2ad1669d6fbd
Create Date: 2018-10-18 10:39:31.709926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f03d57a4d9c0'
down_revision = '2ad1669d6fbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answer', 'create_time')
    # ### end Alembic commands ###
