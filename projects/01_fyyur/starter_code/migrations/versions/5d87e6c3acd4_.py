"""empty message

Revision ID: 5d87e6c3acd4
Revises: 5bd531abdd95
Create Date: 2020-10-12 14:36:53.013919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d87e6c3acd4'
down_revision = '5bd531abdd95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'past_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Artist', 'upcoming_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('Show', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Show', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.drop_column('Show', 'artist_name')
    op.drop_column('Show', 'venue_name')
    op.alter_column('Venue', 'past_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Venue', 'upcoming_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'upcoming_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Venue', 'past_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('Show', sa.Column('venue_name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('artist_name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('Show', 'venue_id')
    op.drop_column('Show', 'artist_id')
    op.alter_column('Artist', 'upcoming_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Artist', 'past_shows',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###