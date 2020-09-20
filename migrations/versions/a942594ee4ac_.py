"""empty message

Revision ID: a942594ee4ac
Revises: e054776ae32a
Create Date: 2020-09-19 20:39:24.171394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a942594ee4ac'
down_revision = 'e054776ae32a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Venue', sa.Column('area', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Venue', 'Area', ['area'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'area')
    op.drop_table('Area')
    # ### end Alembic commands ###