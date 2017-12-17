"""add comment and reply

Revision ID: 76b3748d22fa
Revises: 8092b231e956
Create Date: 2017-12-12 22:19:51.394632

"""

# revision identifiers, used by Alembic.
revision = '76b3748d22fa'
down_revision = '8092b231e956'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('visitor_name', sa.String(length=64), nullable=True),
    sa.Column('visitor_email', sa.String(length=64), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('comment_type', sa.String(length=64), nullable=True),
    sa.Column('reply_to', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('replies',
    sa.Column('replier_id', sa.Integer(), nullable=False),
    sa.Column('replied_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['replied_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['replier_id'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('replier_id', 'replied_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('replies')
    op.drop_table('comments')
    # ### end Alembic commands ###