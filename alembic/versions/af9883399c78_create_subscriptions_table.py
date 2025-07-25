"""create_subscriptions_table

Revision ID: af9883399c78
Revises: a6b9c0f5dafa
Create Date: 2025-07-07 18:03:03.664684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'af9883399c78'
down_revision: Union[str, None] = 'a6b9c0f5dafa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('billing_time', sa.String(length=50), nullable=False),
    sa.Column('replenishment_time', sa.String(length=50), nullable=False),
    sa.Column('frequency', sa.Enum('MONTH', 'YEAR', name='frequencyenum'), nullable=False),
    sa.Column('source', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Enum('COMPLETED', 'PROGRESS', name='statusenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_id'), 'subscriptions', ['id'], unique=False)
    op.alter_column('tasks', 'is_completed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'is_completed',
               existing_type=sa.Integer(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_index(op.f('ix_subscriptions_id'), table_name='subscriptions')
    op.drop_table('subscriptions')
    # ### end Alembic commands ###
