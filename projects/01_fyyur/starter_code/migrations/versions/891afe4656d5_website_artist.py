"""website artist

Revision ID: 891afe4656d5
Revises: 1a07fa092f40
Create Date: 2020-10-18 16:47:09.015474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '891afe4656d5'
down_revision = '1a07fa092f40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website')
    # ### end Alembic commands ###
