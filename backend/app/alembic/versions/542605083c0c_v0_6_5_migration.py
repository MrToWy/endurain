"""v0.6.5 migration

Revision ID: 542605083c0c
Revises: 65a0f1d72997
Create Date: 2024-12-09 16:02:43.332696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = '542605083c0c'
down_revision: Union[str, None] = '65a0f1d72997'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get the current connection
    conn = op.get_bind()

    # Check if the index exists
    index_garminconnect_activity_id_exists = conn.execute(text("""
        SELECT to_regclass('public.garminconnect_activity_id') IS NOT NULL
    """)).scalar()
    index_created_at_exists = conn.execute(text("""
        SELECT to_regclass('public.created_at') IS NOT NULL
    """)).scalar()
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('timezone', sa.String(length=250), nullable=True, comment='Activity timezone (May include spaces)'))
    op.alter_column('activities', 'start_time',
               existing_type=sa.DATETIME(),
               comment='Activity start date (DATETIME)',
               existing_comment='Activity start date (datetime)',
               existing_nullable=False)
    op.alter_column('activities', 'end_time',
               existing_type=sa.DATETIME(),
               comment='Activity end date (DATETIME)',
               existing_comment='Activity end date (datetime)',
               existing_nullable=False)
    op.alter_column('activities', 'total_elapsed_time',
               existing_type=sa.DECIMAL(precision=20, scale=10),
               comment='Activity total elapsed time (s)',
               existing_comment='Activity total elapsed time (datetime)',
               existing_nullable=False)
    op.alter_column('activities', 'total_timer_time',
               existing_type=sa.DECIMAL(precision=20, scale=10),
               comment='Activity total timer time (s)',
               existing_comment='Activity total timer time (datetime)',
               existing_nullable=False)
    op.alter_column('activities', 'created_at',
               existing_type=sa.DATETIME(),
               comment='Activity creation date (DATETIME)',
               existing_comment='Activity creation date (datetime)',
               existing_nullable=False)
    if index_garminconnect_activity_id_exists:
        op.drop_index('garminconnect_activity_id', table_name='activities')
    op.add_column('gear', sa.Column('initial_kms', sa.DECIMAL(precision=11, scale=3), nullable=False, comment='Initial kilometers of the gear'))
    op.alter_column('gear', 'created_at',
               existing_type=sa.DATETIME(),
               comment='Gear creation date (DATETIME)',
               existing_comment='Gear creation date (date)',
               existing_nullable=False)
    op.add_column('health_data', sa.Column('date', sa.Date(), nullable=True, comment='Health data creation date (date)'))
    # Copy data from `created_at` to `date`
    op.execute("""
        UPDATE health_data
        SET date = DATE(created_at)
    """)
    # Make `date` column non-nullable
    op.alter_column('health_data', 'date', nullable=False, comment='Health data creation date (date)', existing_type=sa.Date())
    op.add_column('health_data', sa.Column('bmi', sa.DECIMAL(precision=10, scale=2), nullable=True, comment='Body mass index (BMI)'))
    op.add_column('health_data', sa.Column('garminconnect_body_composition_id', sa.String(length=45), nullable=True, comment='Garmin Connect body composition ID'))
    if index_created_at_exists:
        op.drop_index('created_at', table_name='health_data')
    op.create_unique_constraint(None, 'health_data', ['date'])
    op.drop_column('health_data', 'created_at')
    # Add the new entry to the migrations table
    op.execute("""
    INSERT INTO migrations (id, name, description, executed) VALUES
    (2, 'v0.6.5', 'Process timezone for existing activities', false);
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('health_data', sa.Column('created_at', sa.DATE(), nullable=True, comment='Health data creation date (datetime)'))
    # Copy data back from `date` to `created_at`
    op.execute("""
        UPDATE health_data
        SET created_at = date
    """)
    # Make `created_at` column non-nullable
    op.alter_column('health_data', 'created_at', nullable=False, existing_type=sa.Date())
    op.drop_constraint(None, 'health_data', type_='unique')
    op.create_index('created_at', 'health_data', ['created_at'], unique=True)
    op.drop_column('health_data', 'garminconnect_body_composition_id')
    op.drop_column('health_data', 'bmi')
    op.drop_column('health_data', 'date')
    op.alter_column('gear', 'created_at',
               existing_type=sa.DATETIME(),
               comment='Gear creation date (date)',
               existing_comment='Gear creation date (DATETIME)',
               existing_nullable=False)
    op.drop_column('gear', 'initial_kms')
    op.create_index('garminconnect_activity_id', 'activities', ['garminconnect_activity_id'], unique=True)
    op.alter_column('activities', 'created_at',
               existing_type=sa.DATETIME(),
               comment='Activity creation date (datetime)',
               existing_comment='Activity creation date (DATETIME)',
               existing_nullable=False)
    op.alter_column('activities', 'total_timer_time',
               existing_type=sa.DECIMAL(precision=20, scale=10),
               comment='Activity total timer time (datetime)',
               existing_comment='Activity total timer time (s)',
               existing_nullable=False)
    op.alter_column('activities', 'total_elapsed_time',
               existing_type=sa.DECIMAL(precision=20, scale=10),
               comment='Activity total elapsed time (datetime)',
               existing_comment='Activity total elapsed time (s)',
               existing_nullable=False)
    op.alter_column('activities', 'end_time',
               existing_type=sa.DATETIME(),
               comment='Activity end date (datetime)',
               existing_comment='Activity end date (DATETIME)',
               existing_nullable=False)
    op.alter_column('activities', 'start_time',
               existing_type=sa.DATETIME(),
               comment='Activity start date (datetime)',
               existing_comment='Activity start date (DATETIME)',
               existing_nullable=False)
    op.drop_column('activities', 'timezone')
    # Remove the entry from the migrations table
    op.execute("""
    DELETE FROM migrations 
    WHERE id = 2;
    """)
    # ### end Alembic commands ###
