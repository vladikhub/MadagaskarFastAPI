"""add subscriptions

Revision ID: 230209573ff9
Revises: 945828ec00cb
Create Date: 2025-03-27 23:37:10.211614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '230209573ff9'
down_revision: Union[str, None] = '945828ec00cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('MINUTE', 'UNLIMITED', name='subscriptiontype'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('minute_subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('minutes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['subscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unlimited_subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('period', sa.Enum('MONTH', 'HALF_YEAR', 'YEAR', name='periodtypes'), nullable=True),
    sa.Column('end_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['subscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('clients', sa.Column('subscription_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'clients', 'subscriptions', ['subscription_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clients', type_='foreignkey')
    op.drop_column('clients', 'subscription_id')
    op.drop_table('unlimited_subscriptions')
    op.drop_table('minute_subscriptions')
    op.drop_table('subscriptions')
    # ### end Alembic commands ###
