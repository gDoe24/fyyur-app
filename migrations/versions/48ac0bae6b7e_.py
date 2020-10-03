"""empty message

Revision ID: 48ac0bae6b7e
Revises: a942594ee4ac
Create Date: 2020-09-23 18:24:49.879215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48ac0bae6b7e'
down_revision = 'a942594ee4ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###
