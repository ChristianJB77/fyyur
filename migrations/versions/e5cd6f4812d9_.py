"""empty message

Revision ID: e5cd6f4812d9
Revises: 0b5d97091b03
Create Date: 2020-12-15 22:10:37.599652

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e5cd6f4812d9'
down_revision = '0b5d97091b03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=False))
    op.alter_column('venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)
    op.drop_column('artist', 'genres')
    # ### end Alembic commands ###
