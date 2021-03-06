"""empty message

Revision ID: 219157f190ed
Revises: d88593e0ca24
Create Date: 2020-05-10 21:55:58.528212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '219157f190ed'
down_revision = 'd88593e0ca24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('blog_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('comments', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.Column('parent', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('blogs', sa.Column('body', sa.Text(), nullable=True))
    op.add_column('blogs', sa.Column('category', sa.String(length=100), nullable=True))
    op.add_column('blogs', sa.Column('comments', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('blogs', sa.Column('likes', sa.Integer(), nullable=False))
    op.add_column('blogs', sa.Column('title', sa.Text(), nullable=True))
    op.drop_column('blogs', 'type')
    op.drop_column('blogs', 'msg')
    op.drop_column('blogs', 'subject')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('subject', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('blogs', sa.Column('msg', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('blogs', sa.Column('type', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('blogs', 'title')
    op.drop_column('blogs', 'likes')
    op.drop_column('blogs', 'comments')
    op.drop_column('blogs', 'category')
    op.drop_column('blogs', 'body')
    op.drop_table('comments')
    # ### end Alembic commands ###
