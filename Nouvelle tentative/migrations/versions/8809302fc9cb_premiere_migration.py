"""premiere migration

Revision ID: 8809302fc9cb
Revises: 
Create Date: 2023-11-21 01:03:25.243577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8809302fc9cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('players_limit', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('prompt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=200), nullable=False),
    sa.Column('image_path', sa.String(length=200), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room_user_link',
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('room_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_user_link')
    op.drop_table('prompt')
    op.drop_table('user')
    op.drop_table('room')
    # ### end Alembic commands ###