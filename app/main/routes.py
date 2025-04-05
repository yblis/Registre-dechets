import csv
from datetime import datetime
from io import StringIO
from flask import render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_required, current_user
from app.utils import log_activity
from sqlalchemy import and_, exists
from app import db
from app.main import bp
from app.main.forms import WasteRecordForm, SearchForm
from app.models import WasteRecord, WasteType, Producer, Transporter, TreatmentOperation, EliminationOperation, WasteEntry

@bp.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({"status": "healthy"}), 200

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    query = WasteRecord.query

    # Apply filters if they exist in request args
    if request.args.get('start_date'):
        try:
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
            query = query.filter(WasteRecord.date >= start_date)
        except ValueError:
            pass

    if request.args.get('end_date'):
        try:
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()
            query = query.filter(WasteRecord.date <= end_date)
        except ValueError:
            pass

    if request.args.get('waste_type_id') and request.args.get('waste_type_id').isdigit():
        waste_type_id = int(request.args.get('waste_type_id'))
        query = query.join(WasteEntry).filter(WasteEntry.waste_type_id == waste_type_id)

    if request.args.get('producer_id') and request.args.get('producer_id').isdigit():
        query = query.filter(WasteRecord.producer_id == int(request.args.get('producer_id')))

    if request.args.get('destination'):
        query = query.filter(WasteRecord.destination.ilike(f"%{request.args.get('destination')}%"))

    if request.args.get('transporter_id') and request.args.get('transporter_id').isdigit():
        query = query.filter(WasteRecord.transporter_id == int(request.args.get('transporter_id')))

    # Order by date descending
    records = query.order_by(WasteRecord.date.desc()).paginate(page=page, per_page=10)
    return render_template('main/index.html', title='Registre des déchets',
                         records=records, search_form=search_form)

@bp.route('/record/new', methods=['GET', 'POST'])
@login_required
def create_record():
    form = WasteRecordForm()
    if form.validate_on_submit():
        record = WasteRecord(
            date=form.date.data,
            producer_id=form.producer_id.data,
            destination=form.destination.data,
            transporter_id=form.transporter_id.data,
            treatment_operation_id=form.treatment_operation_id.data,
            elimination_operation_id=form.elimination_operation_id.data or None,
            tracking_number=form.tracking_number.data,
            notes=form.notes.data,
            author=current_user
        )
        for entry_form in form.waste_entries:
            waste_entry = WasteEntry(
                waste_type_id=entry_form.waste_type_id.data,
                quantity=entry_form.quantity.data,
                unit=entry_form.unit.data
            )
            record.waste_entries.append(waste_entry)
            
        db.session.add(record)
        try:
            db.session.commit()
            log_activity('create', 'WasteRecord', record.id, {
                'tracking_number': record.tracking_number,
                'waste_types': [{'id': entry.waste_type_id, 'quantity': entry.quantity, 'unit': entry.unit} 
                              for entry in record.waste_entries],
                'date': record.date.strftime('%Y-%m-%d')
            })
            flash('Enregistrement créé avec succès.', 'success')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('Erreur: Le numéro de bordereau doit être unique.', 'danger')
            return redirect(url_for('main.create_record'))
    return render_template('main/record_form.html', title='Nouvel enregistrement',
                         form=form)

@bp.route('/record/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    record = WasteRecord.query.get_or_404(id)
    if request.method == 'GET':
        form = WasteRecordForm(obj=record)
        # Populate waste entries
        while len(form.waste_entries) > 0:
            form.waste_entries.pop_entry()
        for entry in record.waste_entries:
            form.waste_entries.append_entry({
                'waste_type_id': entry.waste_type_id,
                'quantity': entry.quantity,
                'unit': entry.unit
            })
    else:
        form = WasteRecordForm()
        if form.validate_on_submit():
            record.date = form.date.data
            record.producer_id = form.producer_id.data
            record.destination = form.destination.data
            record.transporter_id = form.transporter_id.data
            record.treatment_operation_id = form.treatment_operation_id.data
            record.elimination_operation_id = form.elimination_operation_id.data or None
            record.tracking_number = form.tracking_number.data
            record.notes = form.notes.data
            
            # Clear existing entries and add new ones
            record.waste_entries.delete()
            for entry_form in form.waste_entries:
                waste_entry = WasteEntry(
                    waste_type_id=entry_form.waste_type_id.data,
                    quantity=entry_form.quantity.data,
                    unit=entry_form.unit.data
                )
                record.waste_entries.append(waste_entry)
            
            try:
                db.session.commit()
                log_activity('update', 'WasteRecord', record.id, {
                    'tracking_number': record.tracking_number,
                    'waste_types': [{'id': entry.waste_type_id, 'quantity': entry.quantity, 'unit': entry.unit} 
                                  for entry in record.waste_entries],
                    'date': record.date.strftime('%Y-%m-%d')
                })
                flash('Enregistrement modifié avec succès.', 'success')
                return redirect(url_for('main.index'))
            except:
                db.session.rollback()
                flash('Erreur: Le numéro de bordereau doit être unique.', 'danger')
    return render_template('main/record_form.html', title='Modifier l\'enregistrement',
                         form=form)

@bp.route('/record/<int:id>/delete', methods=['POST'])
@login_required
def delete_record(id):
    record = WasteRecord.query.get_or_404(id)
    tracking_number = record.tracking_number
    waste_types = [{'id': entry.waste_type_id, 'quantity': entry.quantity, 'unit': entry.unit} 
                  for entry in record.waste_entries]
    db.session.delete(record)
    db.session.commit()
    log_activity('delete', 'WasteRecord', id, {
        'tracking_number': tracking_number,
        'waste_types': waste_types
    })
    flash('Enregistrement supprimé avec succès.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/export')
@login_required
def export_csv():
    # Build query with filters
    query = WasteRecord.query

    if request.args.get('start_date'):
        try:
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
            query = query.filter(WasteRecord.date >= start_date)
        except ValueError:
            pass

    if request.args.get('end_date'):
        try:
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()
            query = query.filter(WasteRecord.date <= end_date)
        except ValueError:
            pass

    if request.args.get('waste_type_id') and request.args.get('waste_type_id').isdigit():
        waste_type_id = int(request.args.get('waste_type_id'))
        query = query.join(WasteEntry).filter(WasteEntry.waste_type_id == waste_type_id)

    if request.args.get('producer_id') and request.args.get('producer_id').isdigit():
        query = query.filter(WasteRecord.producer_id == int(request.args.get('producer_id')))

    if request.args.get('destination'):
        query = query.filter(WasteRecord.destination.ilike(f"%{request.args.get('destination')}%"))

    if request.args.get('transporter_id') and request.args.get('transporter_id').isdigit():
        query = query.filter(WasteRecord.transporter_id == int(request.args.get('transporter_id')))

    # Get records ordered by date
    records = query.order_by(WasteRecord.date.desc()).all()

    # Create CSV file
    si = StringIO()
    cw = csv.writer(si)
    
    # Write headers
    cw.writerow(['Date', 'Type de déchet', 'Code déchet', 'Dangereux', 'Quantité', 'Unité', 
                 'Producteur', 'SIRET Producteur', 'Destination', 'Transporteur', 
                 'SIRET Transporteur', 'Immatriculation', 'Opération de traitement',
                 'Opération d\'élimination', 'N° Bordereau', 'Remarques'])
    
    # Write records - one line per waste entry
    for record in records:
        for waste_entry in record.waste_entries:
            cw.writerow([
                record.date.strftime('%Y-%m-%d'),
                waste_entry.waste_type_ref.description,
                waste_entry.waste_type_ref.code,
                'Oui' if waste_entry.waste_type_ref.dangerous else 'Non',
                waste_entry.quantity,
                waste_entry.unit,
                record.producer_ref.name,
                record.producer_ref.siret,
                record.destination,
                record.transporter_ref.name,
                record.transporter_ref.siret,
                record.transporter_ref.registration,
                f"{record.treatment_operation_ref.code} - {record.treatment_operation_ref.description}",
                f"{record.elimination_operation_ref.code} - {record.elimination_operation_ref.description}" if record.elimination_operation_ref else "",
                record.tracking_number,
                record.notes
            ])

    output = si.getvalue()
    si.close()
    
    # Utiliser BytesIO au lieu de StringIO pour le mode binaire
    from io import BytesIO
    buffer = BytesIO()
    buffer.write(output.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'registre_dechets_{datetime.now().strftime("%Y%m%d")}.csv'
    )
