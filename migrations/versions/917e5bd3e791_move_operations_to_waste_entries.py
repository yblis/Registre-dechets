"""Move operations to waste entries

Revision ID: 917e5bd3e791
Revises: 9bc8743fd093
Create Date: 2025-04-05 22:06:59.528350

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.models import WasteRecord, WasteEntry
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '917e5bd3e791'
down_revision = '9bc8743fd093'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to waste_entry
    with op.batch_alter_table('waste_entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('treatment_operation_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('elimination_operation_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'treatment_operation', ['treatment_operation_id'], ['id'])
        batch_op.create_foreign_key(None, 'elimination_operation', ['elimination_operation_id'], ['id'])

    # Migrate data from waste_record to waste_entry
    try:
        bind = op.get_bind()
        session = Session(bind=bind)
        
        # Copy operation IDs from waste_record to its waste_entries
        for record in session.query(WasteRecord).all():
            for entry in record.waste_entries:
                entry.treatment_operation_id = record.treatment_operation_id
                entry.elimination_operation_id = record.elimination_operation_id
        session.commit()
    except Exception as e:
        print(f"Erreur lors de la migration des données: {e}")
        # Continue despite error, as we may be in a fresh install

    # Make treatment_operation_id not nullable after data migration
    with op.batch_alter_table('waste_entry', schema=None) as batch_op:
        batch_op.alter_column('treatment_operation_id', nullable=False)

    # Instead of recreating the waste_record table, just drop the columns directly
    # Check if columns exist before trying to drop them
    conn = op.get_bind()
    try:
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'waste_record' AND column_name IN ('treatment_operation_id', 'elimination_operation_id')"))
        columns = [row[0] for row in result]
        
        # Use separate batch_alter_table operations for each column to avoid recreating the table
        if 'treatment_operation_id' in columns:
            with op.batch_alter_table('waste_record', schema=None) as batch_op:
                batch_op.drop_column('treatment_operation_id')
                
        if 'elimination_operation_id' in columns:
            with op.batch_alter_table('waste_record', schema=None) as batch_op:
                batch_op.drop_column('elimination_operation_id')
    except Exception as e:
        print(f"Error modifying waste_record table: {e}")


def downgrade():
    # Add back columns to waste_record
    with op.batch_alter_table('waste_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('treatment_operation_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('elimination_operation_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_waste_record_treatment_operation_id_treatment_operation', 'treatment_operation', ['treatment_operation_id'], ['id'])
        batch_op.create_foreign_key('fk_waste_record_elimination_operation_id_elimination_operation', 'elimination_operation', ['elimination_operation_id'], ['id'])

    try:
        # Copy data back from waste_entry to waste_record
        bind = op.get_bind()
        session = Session(bind=bind)
        
        # For each waste_record, take operation IDs from its first waste_entry
        for record in session.query(WasteRecord).all():
            first_entry = record.waste_entries.first()
            if first_entry:
                record.treatment_operation_id = first_entry.treatment_operation_id
                record.elimination_operation_id = first_entry.elimination_operation_id
        session.commit()
    except Exception as e:
        print(f"Erreur lors de la migration inverse des données: {e}")
        # Continue despite error

    # Make treatment_operation_id not nullable
    with op.batch_alter_table('waste_record', schema=None) as batch_op:
        batch_op.alter_column('treatment_operation_id', nullable=False)

    # Remove columns from waste_entry
    with op.batch_alter_table('waste_entry', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('elimination_operation_id')
        batch_op.drop_column('treatment_operation_id')
