"""empty message

Revision ID: a1cb4532bc65
Revises: 8665d1acba77
Create Date: 2020-10-19 14:19:59.842198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1cb4532bc65'
down_revision = '8665d1acba77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('book_records_batch_id_fkey', 'book_records', type_='foreignkey')
    op.drop_column('book_records', 'batch_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_records', sa.Column('batch_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('book_records_batch_id_fkey', 'book_records', 'batch', ['batch_id'], ['batch_id'])
    # ### end Alembic commands ###