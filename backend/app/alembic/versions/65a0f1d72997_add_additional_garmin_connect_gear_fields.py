"""Add additional Garmin Connect gear fields

Revision ID: 65a0f1d72997
Revises: 241bdc784fef
Create Date: 2024-11-20 21:38:54.888855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65a0f1d72997'
down_revision: Union[str, None] = '241bdc784fef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('garminconnect_gear_id', sa.String(length=45), nullable=True, comment='Garmin Connect gear ID'))
    op.add_column('gear', sa.Column('garminconnect_gear_id', sa.String(length=45), nullable=True, comment='Garmin Connect gear ID'))
    op.create_unique_constraint(None, 'gear', ['garminconnect_gear_id'])
    op.add_column('users_integrations', sa.Column('garminconnect_sync_gear', sa.Boolean(), nullable=False, comment='Whether Garmin Connect gear is to be synced'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_integrations', 'garminconnect_sync_gear')
    op.drop_constraint(None, 'gear', type_='unique')
    op.drop_column('gear', 'garminconnect_gear_id')
    op.drop_column('activities', 'garminconnect_gear_id')
    # ### end Alembic commands ###
