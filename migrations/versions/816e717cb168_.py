"""empty message

Revision ID: 816e717cb168
Revises: 2be27845ba99
Create Date: 2020-12-14 21:49:25.035610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '816e717cb168'
down_revision = '2be27845ba99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'seeking_talent',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'seeking_talent',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###