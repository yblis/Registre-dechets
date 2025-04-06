from flask import jsonify, request
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_login import login_required
from app import db
from app.main import bp
from app.models import Producer, Transporter

@bp.route('/api/producer/add', methods=['POST'])
@login_required
def add_producer_ajax():
    try:
        # Validate CSRF token
        token = request.headers.get('X-CSRFToken')
        if not token:
            return jsonify({'success': False, 'error': 'CSRF token manquant'})
        try:
            validate_csrf(token)
        except ValidationError:
            return jsonify({'success': False, 'error': 'Token CSRF invalide'})
        # Valider les données
        name = request.form.get('name')
        siret = request.form.get('siret')
        address = request.form.get('address')
        
        if not all([name, siret, address]) or len(siret) != 14:
            return jsonify({'success': False, 'error': 'Données invalides'})
        
        # Vérifier si le SIRET existe déjà
        if Producer.query.filter_by(siret=siret).first():
            return jsonify({'success': False, 'error': 'Ce numéro SIRET existe déjà'})
        
        # Créer le producteur
        producer = Producer(name=name, siret=siret, address=address)
        db.session.add(producer)
        db.session.commit()
        
        # Retourner les données pour mettre à jour le select
        return jsonify({
            'success': True,
            'id': producer.id,
            'label': f"{producer.name} ({producer.siret})"
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api/transporter/add', methods=['POST'])
@login_required
def add_transporter_ajax():
    try:
        # Validate CSRF token
        token = request.headers.get('X-CSRFToken')
        if not token:
            return jsonify({'success': False, 'error': 'CSRF token manquant'})
        try:
            validate_csrf(token)
        except ValidationError:
            return jsonify({'success': False, 'error': 'Token CSRF invalide'})
        # Valider les données
        name = request.form.get('name')
        siret = request.form.get('siret')
        address = request.form.get('address')
        registration = request.form.get('registration')
        
        if not all([name, siret, address, registration]) or len(siret) != 14:
            return jsonify({'success': False, 'error': 'Données invalides'})
        
        # Vérifier si le SIRET existe déjà
        if Transporter.query.filter_by(siret=siret).first():
            return jsonify({'success': False, 'error': 'Ce numéro SIRET existe déjà'})
        
        # Créer le transporteur
        transporter = Transporter(
            name=name,
            siret=siret,
            address=address,
            registration=registration
        )
        db.session.add(transporter)
        db.session.commit()
        
        # Retourner les données pour mettre à jour le select
        return jsonify({
            'success': True,
            'id': transporter.id,
            'label': f"{transporter.name} ({transporter.registration})"
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
