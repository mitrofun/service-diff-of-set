# type: ignore
"""add result values

Revision ID: f575ba3e4325
Revises:
Create Date: 2021-04-30 14:23:44.745463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f575ba3e4325'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_calculations_status', table_name='calculations')
    op.drop_table('calculations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calculations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('file', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('status', sa.INTEGER(), nullable=True),
    sa.Column('create_at', sa.DATETIME(), nullable=True),
    sa.Column('finished_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_calculations_status', 'calculations', ['status'], unique=False)
    # ### end Alembic commands ###
