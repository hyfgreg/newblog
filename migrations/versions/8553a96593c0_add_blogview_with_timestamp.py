"""add blogview with timestamp

Revision ID: 8553a96593c0
Revises: 5115afc51c0a
Create Date: 2017-11-17 23:54:27.687355

"""

# revision identifiers, used by Alembic.
revision = '8553a96593c0'
down_revision = '5115afc51c0a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_view', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_blog_view_timestamp'), 'blog_view', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_view_timestamp'), table_name='blog_view')
    op.drop_column('blog_view', 'timestamp')
    # ### end Alembic commands ###
