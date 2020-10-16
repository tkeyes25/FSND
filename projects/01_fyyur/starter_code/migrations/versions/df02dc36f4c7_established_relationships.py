"""Established relationships

Revision ID: df02dc36f4c7
Revises: b45db1c49238
Create Date: 2020-10-15 15:25:48.201462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df02dc36f4c7'
down_revision = 'b45db1c49238'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Artist_upcoming_shows_fkey', 'Artist', type_='foreignkey')
    op.drop_constraint('Artist_past_shows_fkey', 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'upcoming_shows')
    op.drop_column('Artist', 'past_shows')
    op.drop_constraint('Venue_upcoming_shows_fkey', 'Venue', type_='foreignkey')
    op.drop_constraint('Venue_past_shows_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'upcoming_shows')
    op.drop_column('Venue', 'past_shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('past_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Venue_past_shows_fkey', 'Venue', 'Show', ['past_shows'], ['id'])
    op.create_foreign_key('Venue_upcoming_shows_fkey', 'Venue', 'Show', ['upcoming_shows'], ['id'])
    op.add_column('Artist', sa.Column('past_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Artist_past_shows_fkey', 'Artist', 'Show', ['past_shows'], ['id'])
    op.create_foreign_key('Artist_upcoming_shows_fkey', 'Artist', 'Show', ['upcoming_shows'], ['id'])
    # ### end Alembic commands ###
