"""empty message

Revision ID: ea49884945e1
Revises: e5cd6f4812d9
Create Date: 2020-12-21 17:35:38.052856

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ea49884945e1'
down_revision = 'e5cd6f4812d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.String(length=5), nullable=True),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_talent', sa.String(length=5), nullable=True),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('fyyur')
    op.drop_table('show')
    op.drop_table('venue')
    op.drop_table('artist')


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fyyur',
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('show_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='fyyur_artist_id_fkey'),
    sa.ForeignKeyConstraint(['show_id'], ['show.id'], name='fyyur_show_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='fyyur_venue_id_fkey')
    )
    op.create_table('show',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='show_pkey')
    )
    op.create_table('artist',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.VARCHAR(length=120)), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='artist_pkey')
    )
    op.create_table('venue',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('seeking_talent', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.VARCHAR(length=120)), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='venue_pkey')
    )
    op.drop_table('shows')
    op.drop_table('venues')
    op.drop_table('artists')
    # ### end Alembic commands ###