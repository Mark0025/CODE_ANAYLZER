"""Initial database setup

Revision ID: initial_setup
Revises: 
Create Date: 2024-11-27 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers
revision = 'initial_setup'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create tables
    op.create_table(
        'crew_outputs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crew_name', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('output_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('results', sqlite.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes
    op.create_index('idx_crew_outputs_timestamp', 'crew_outputs', ['timestamp'])
    op.create_index('idx_crew_outputs_status', 'crew_outputs', ['status'])
    
    # Create error handling results table
    op.create_table(
        'error_handling_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crew_output_id', sa.Integer(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('changes_made', sqlite.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['crew_output_id'], ['crew_outputs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes
    op.create_index('idx_error_results_status', 'error_handling_results', ['status'])

def downgrade():
    # Remove indexes
    op.drop_index('idx_error_results_status')
    op.drop_index('idx_crew_outputs_status')
    op.drop_index('idx_crew_outputs_timestamp')
    
    # Remove tables
    op.drop_table('error_handling_results')
    op.drop_table('crew_outputs') 