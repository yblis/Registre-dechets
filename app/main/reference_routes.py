from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app import db
from app.utils import log_activity
from app.utils.import_export import ImportExportManager
from app.main import bp
from app.models import WasteType, Producer, Transporter, TreatmentOperation, EliminationOperation
from app.main.reference_forms import (WasteTypeForm, ProducerForm, TransporterForm,
                                    TreatmentOperationForm, EliminationOperationForm,
                                    ImportForm)

# Waste Types
@bp.route('/waste-types')
@login_required
def list_waste_types():
    page = request.args.get('page', 1, type=int)
    items = WasteType.query.order_by(WasteType.code).paginate(page=page, per_page=10)
    form = WasteTypeForm()
    import_form = ImportForm()
    return render_template('main/waste_types.html', items=items, form=form, import_form=import_form, entity_type='waste_types')

@bp.route('/waste-types/add', methods=['POST'])
@login_required
def add_waste_type():
    form = WasteTypeForm()
    if form.validate_on_submit():
        waste_type = WasteType(
            code=form.code.data,
            description=form.description.data,
            dangerous=form.dangerous.data
        )
        db.session.add(waste_type)
        try:
            db.session.commit()
            log_activity('create', 'WasteType', waste_type.id, {
                'code': waste_type.code,
                'description': waste_type.description
            })
            flash('Type de déchet ajouté avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout du type de déchet.', 'danger')
    return redirect(url_for('main.list_waste_types'))

@bp.route('/waste-types/<int:id>/edit', methods=['POST'])
@login_required
def edit_waste_type(id):
    waste_type = WasteType.query.get_or_404(id)
    form = WasteTypeForm()
    form._obj_id = id
    if form.validate_on_submit():
        waste_type.code = form.code.data
        waste_type.description = form.description.data
        waste_type.dangerous = form.dangerous.data
        try:
            db.session.commit()
            log_activity('update', 'WasteType', waste_type.id, {
                'code': waste_type.code,
                'description': waste_type.description
            })
            flash('Type de déchet modifié avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de la modification du type de déchet.', 'danger')
    return redirect(url_for('main.list_waste_types'))

@bp.route('/waste-types/<int:id>/delete', methods=['POST'])
@login_required
def delete_waste_type(id):
    waste_type = WasteType.query.get_or_404(id)
    try:
        code = waste_type.code
        db.session.delete(waste_type)
        db.session.commit()
        log_activity('delete', 'WasteType', id, {'code': code})
        flash('Type de déchet supprimé avec succès.', 'success')
    except:
        db.session.rollback()
        flash('Impossible de supprimer ce type de déchet car il est utilisé dans des enregistrements.', 'danger')
    return redirect(url_for('main.list_waste_types'))

# Producers
@bp.route('/producers')
@login_required
def list_producers():
    page = request.args.get('page', 1, type=int)
    items = Producer.query.order_by(Producer.name).paginate(page=page, per_page=10)
    form = ProducerForm()
    import_form = ImportForm()
    return render_template('main/producers.html', items=items, form=form, import_form=import_form, entity_type='producers')

@bp.route('/producers/add', methods=['POST'])
@login_required
def add_producer():
    form = ProducerForm()
    if form.validate_on_submit():
        producer = Producer(
            name=form.name.data,
            siret=form.siret.data,
            address=form.address.data
        )
        db.session.add(producer)
        try:
            db.session.commit()
            log_activity('create', 'Producer', producer.id, {
                'name': producer.name,
                'siret': producer.siret
            })
            flash('Producteur ajouté avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout du producteur.', 'danger')
    return redirect(url_for('main.list_producers'))

@bp.route('/producers/<int:id>/edit', methods=['POST'])
@login_required
def edit_producer(id):
    producer = Producer.query.get_or_404(id)
    form = ProducerForm()
    form._obj_id = id
    if form.validate_on_submit():
        producer.name = form.name.data
        producer.siret = form.siret.data
        producer.address = form.address.data
        try:
            db.session.commit()
            log_activity('update', 'Producer', producer.id, {
                'name': producer.name,
                'siret': producer.siret
            })
            flash('Producteur modifié avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de la modification du producteur.', 'danger')
    return redirect(url_for('main.list_producers'))

@bp.route('/producers/<int:id>/delete', methods=['POST'])
@login_required
def delete_producer(id):
    producer = Producer.query.get_or_404(id)
    try:
        name = producer.name
        siret = producer.siret
        db.session.delete(producer)
        db.session.commit()
        log_activity('delete', 'Producer', id, {
            'name': name,
            'siret': siret
        })
        flash('Producteur supprimé avec succès.', 'success')
    except:
        db.session.rollback()
        flash('Impossible de supprimer ce producteur car il est utilisé dans des enregistrements.', 'danger')
    return redirect(url_for('main.list_producers'))

# Transporters
@bp.route('/transporters')
@login_required
def list_transporters():
    page = request.args.get('page', 1, type=int)
    items = Transporter.query.order_by(Transporter.name).paginate(page=page, per_page=10)
    form = TransporterForm()
    import_form = ImportForm()
    return render_template('main/transporters.html', items=items, form=form, import_form=import_form, entity_type='transporters')

@bp.route('/transporters/add', methods=['POST'])
@login_required
def add_transporter():
    form = TransporterForm()
    if form.validate_on_submit():
        transporter = Transporter(
            name=form.name.data,
            siret=form.siret.data,
            address=form.address.data,
            registration=form.registration.data
        )
        db.session.add(transporter)
        try:
            db.session.commit()
            log_activity('create', 'Transporter', transporter.id, {
                'name': transporter.name,
                'siret': transporter.siret,
                'registration': transporter.registration
            })
            flash('Transporteur ajouté avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout du transporteur.', 'danger')
    return redirect(url_for('main.list_transporters'))

@bp.route('/transporters/<int:id>/edit', methods=['POST'])
@login_required
def edit_transporter(id):
    transporter = Transporter.query.get_or_404(id)
    form = TransporterForm()
    form._obj_id = id
    if form.validate_on_submit():
        transporter.name = form.name.data
        transporter.siret = form.siret.data
        transporter.address = form.address.data
        transporter.registration = form.registration.data
        try:
            db.session.commit()
            log_activity('update', 'Transporter', transporter.id, {
                'name': transporter.name,
                'siret': transporter.siret,
                'registration': transporter.registration
            })
            flash('Transporteur modifié avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de la modification du transporteur.', 'danger')
    return redirect(url_for('main.list_transporters'))

@bp.route('/transporters/<int:id>/delete', methods=['POST'])
@login_required
def delete_transporter(id):
    transporter = Transporter.query.get_or_404(id)
    try:
        name = transporter.name
        registration = transporter.registration
        db.session.delete(transporter)
        db.session.commit()
        log_activity('delete', 'Transporter', id, {
            'name': name,
            'registration': registration
        })
        flash('Transporteur supprimé avec succès.', 'success')
    except:
        db.session.rollback()
        flash('Impossible de supprimer ce transporteur car il est utilisé dans des enregistrements.', 'danger')
    return redirect(url_for('main.list_transporters'))

# Treatment Operations
@bp.route('/treatment-operations')
@login_required
def list_treatment_operations():
    page = request.args.get('page', 1, type=int)
    items = TreatmentOperation.query.order_by(TreatmentOperation.code).paginate(page=page, per_page=10)
    form = TreatmentOperationForm()
    import_form = ImportForm()
    return render_template('main/treatment_operations.html', items=items, form=form, import_form=import_form, entity_type='treatment_operations')

@bp.route('/treatment-operations/add', methods=['POST'])
@login_required
def add_treatment_operation():
    form = TreatmentOperationForm()
    if form.validate_on_submit():
        operation = TreatmentOperation(
            code=form.code.data,
            description=form.description.data
        )
        db.session.add(operation)
        try:
            db.session.commit()
            log_activity('create', 'TreatmentOperation', operation.id, {
                'code': operation.code,
                'description': operation.description
            })
            flash('Opération de traitement ajoutée avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout de l\'opération de traitement.', 'danger')
    return redirect(url_for('main.list_treatment_operations'))

@bp.route('/treatment-operations/<int:id>/edit', methods=['POST'])
@login_required
def edit_treatment_operation(id):
    operation = TreatmentOperation.query.get_or_404(id)
    form = TreatmentOperationForm()
    form._obj_id = id
    if form.validate_on_submit():
        operation.code = form.code.data
        operation.description = form.description.data
        try:
            db.session.commit()
            log_activity('update', 'TreatmentOperation', operation.id, {
                'code': operation.code,
                'description': operation.description
            })
            flash('Opération de traitement modifiée avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de la modification de l\'opération de traitement.', 'danger')
    return redirect(url_for('main.list_treatment_operations'))

@bp.route('/treatment-operations/<int:id>/delete', methods=['POST'])
@login_required
def delete_treatment_operation(id):
    operation = TreatmentOperation.query.get_or_404(id)
    try:
        code = operation.code
        db.session.delete(operation)
        db.session.commit()
        log_activity('delete', 'TreatmentOperation', id, {'code': code})
        flash('Opération de traitement supprimée avec succès.', 'success')
    except:
        db.session.rollback()
        flash('Impossible de supprimer cette opération car elle est utilisée dans des enregistrements.', 'danger')
    return redirect(url_for('main.list_treatment_operations'))

# Elimination Operations
@bp.route('/elimination-operations')
@login_required
def list_elimination_operations():
    page = request.args.get('page', 1, type=int)
    items = EliminationOperation.query.order_by(EliminationOperation.code).paginate(page=page, per_page=10)
    form = EliminationOperationForm()
    import_form = ImportForm()
    return render_template('main/elimination_operations.html', items=items, form=form, import_form=import_form, entity_type='elimination_operations')

@bp.route('/elimination-operations/add', methods=['POST'])
@login_required
def add_elimination_operation():
    form = EliminationOperationForm()
    if form.validate_on_submit():
        operation = EliminationOperation(
            code=form.code.data,
            description=form.description.data
        )
        db.session.add(operation)
        try:
            db.session.commit()
            log_activity('create', 'EliminationOperation', operation.id, {
                'code': operation.code,
                'description': operation.description
            })
            flash('Opération d\'élimination ajoutée avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout de l\'opération d\'élimination.', 'danger')
    return redirect(url_for('main.list_elimination_operations'))

# Import/Export Routes
@bp.route('/reference/export/<entity_type>')
@login_required
def export_reference_data(entity_type):
    """Export des données de référence au format CSV."""
    from app.utils.import_export import ImportExportManager
    try:
        data = ImportExportManager.export_data(entity_type)
        return send_file(
            data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{entity_type}.csv'
        )
    except Exception as e:
        flash(f'Erreur lors de l\'export : {str(e)}', 'danger')
        return redirect(request.referrer)

@bp.route('/reference/export/<entity_type>/excel')
@login_required
def export_reference_data_excel(entity_type):
    """Export des données de référence au format Excel."""
    from app.utils.import_export import ImportExportManager
    try:
        output = ImportExportManager.export_excel(entity_type)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{entity_type}.xlsx'
        )
    except Exception as e:
        flash(f'Erreur lors de l\'export Excel : {str(e)}', 'danger')
        return redirect(request.referrer)

@bp.route('/reference/template/<entity_type>')
@login_required
def get_reference_template(entity_type):
    """Téléchargement du modèle d'import."""
    from app.utils.import_export import ImportExportManager
    try:
        template = ImportExportManager.get_template(entity_type)
        return send_file(
            template,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{entity_type}_template.csv'
        )
    except Exception as e:
        flash(f'Erreur lors du téléchargement du modèle : {str(e)}', 'danger')
        return redirect(request.referrer)

@bp.route('/reference/import/<entity_type>', methods=['POST'])
@login_required
def import_reference_data(entity_type):
    """Import de données de référence depuis un fichier CSV."""
    from app.utils.import_export import ImportExportManager
    
    form = ImportForm()
    if not form.validate_on_submit():
        flash('Formulaire invalide', 'danger')
        return redirect(request.referrer)

    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(request.referrer)
        
    file = request.files['file']
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(request.referrer)
        
    if not file.filename.endswith('.csv'):
        flash('Format de fichier non supporté. Utilisez un fichier CSV.', 'danger')
        return redirect(request.referrer)
        
    try:
        results = ImportExportManager.import_data(entity_type, file)
        if results['errors']:
            flash(f'Import terminé avec {len(results["errors"])} erreurs. '
                  f'Créés : {results["created"]}, Mis à jour : {results["updated"]}', 'warning')
            for error in results['errors']:
                flash(error, 'danger')
        else:
            flash(f'Import réussi. Créés : {results["created"]}, '
                  f'Mis à jour : {results["updated"]}', 'success')
    except Exception as e:
        flash(f'Erreur lors de l\'import : {str(e)}', 'danger')
        
    return redirect(request.referrer or url_for('main.list_' + entity_type))

@bp.route('/elimination-operations/<int:id>/edit', methods=['POST'])
@login_required
def edit_elimination_operation(id):
    operation = EliminationOperation.query.get_or_404(id)
    form = EliminationOperationForm()
    form._obj_id = id
    if form.validate_on_submit():
        operation.code = form.code.data
        operation.description = form.description.data
        try:
            db.session.commit()
            log_activity('update', 'EliminationOperation', operation.id, {
                'code': operation.code,
                'description': operation.description
            })
            flash('Opération d\'élimination modifiée avec succès.', 'success')
        except:
            db.session.rollback()
            flash('Erreur lors de la modification de l\'opération d\'élimination.', 'danger')
    return redirect(url_for('main.list_elimination_operations'))

@bp.route('/elimination-operations/<int:id>/delete', methods=['POST'])
@login_required
def delete_elimination_operation(id):
    operation = EliminationOperation.query.get_or_404(id)
    try:
        code = operation.code
        db.session.delete(operation)
        db.session.commit()
        log_activity('delete', 'EliminationOperation', id, {'code': code})
        flash('Opération d\'élimination supprimée avec succès.', 'success')
    except:
        db.session.rollback()
        flash('Impossible de supprimer cette opération car elle est utilisée dans des enregistrements.', 'danger')
    return redirect(url_for('main.list_elimination_operations'))
