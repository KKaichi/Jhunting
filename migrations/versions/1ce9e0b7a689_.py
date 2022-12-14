"""empty message

Revision ID: 1ce9e0b7a689
Revises: a3fb86270efd
Create Date: 2022-09-29 12:32:41.299191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ce9e0b7a689'
down_revision = 'a3fb86270efd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('company_id', sa.String(), nullable=True),
    sa.Column('event_name', sa.String(), nullable=True),
    sa.Column('start_day', sa.Date(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('memo', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_event_name'), 'events', ['event_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_events_event_name'), table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###
