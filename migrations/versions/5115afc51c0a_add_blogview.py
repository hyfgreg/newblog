"""add blogview

Revision ID: 5115afc51c0a
Revises: 4f420d20d674
Create Date: 2017-11-17 23:52:15.929993

"""

# revision identifiers, used by Alembic.
revision = '5115afc51c0a'
down_revision = '4f420d20d674'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num_of_view', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_view')
    # ### end Alembic commands ###