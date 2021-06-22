"""The Project's Schema

Revision ID: 35873e6cd829
Revises: 
Create Date: 2021-06-20 13:39:24.939780

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '35873e6cd829'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('city', sa.String(length=120), nullable=True),
                    sa.Column('state', sa.String(length=120), nullable=True),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('website_link', sa.String(length=120), nullable=True),
                    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
                    sa.Column('seeking_description', sa.String(length=120), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Genre',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('genre', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Venue',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('city', sa.String(length=120), nullable=True),
                    sa.Column('state', sa.String(length=120), nullable=True),
                    sa.Column('address', sa.String(length=120), nullable=True),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('website_link', sa.String(length=120), nullable=True),
                    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
                    sa.Column('seeking_description', sa.String(length=120), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('artist_genre',
                    sa.Column('genre_id', sa.Integer(), nullable=True),
                    sa.Column('artist_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ondelete='CASCADE')
                    )
    op.create_table('show',
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.Column('start_time', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('artist_id', 'venue_id', 'start_time')
                    )
    op.create_table('venue_genre',
                    sa.Column('genre_id', sa.Integer(), nullable=True),
                    sa.Column('venue_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ondelete='CASCADE')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_genre')
    op.drop_table('show')
    op.drop_table('artist_genre')
    op.drop_table('Venue')
    op.drop_table('Genre')
    op.drop_table('Artist')
    # ### end Alembic commands ###
