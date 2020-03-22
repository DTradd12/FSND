"""empty message

Revision ID: a285328398ef
Revises: b1f5414ac65a
Create Date: 2020-03-22 13:55:59.723571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a285328398ef'
down_revision = 'b1f5414ac65a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('artist', sa.Column(
        'created_at', sa.DateTime(), nullable=True))
    op.add_column('venue', sa.Column(
        'created_at', sa.DateTime(), nullable=True))

    op.execute(
        'UPDATE artist SET created_at= CURRENT_TIMESTAMP WHERE created_at IS NULL')
    op.execute(
        'UPDATE venue SET created_at= CURRENT_TIMESTAMP WHERE created_at IS NULL')

    op.alter_column('artist', 'created_at', nullable=False)
    op.alter_column('venue', 'created_at', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'created_at')
    op.drop_column('artist', 'created_at')
    # ### end Alembic commands ###
