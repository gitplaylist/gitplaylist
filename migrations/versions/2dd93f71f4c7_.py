"""empty message

Revision ID: 2dd93f71f4c7
Revises: 93b4d7a531de
Create Date: 2016-05-29 21:08:21.155741

"""

# revision identifiers, used by Alembic.
revision = '2dd93f71f4c7'
down_revision = '93b4d7a531de'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=32), nullable=True))
    op.create_unique_constraint(None, 'users', ['username'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    ### end Alembic commands ###
