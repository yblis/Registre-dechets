from flask import render_template, request, abort
from flask_login import login_required
from app.main import bp
from app.admin.decorators import admin_required
from app.models import ActivityLog, User
from sqlalchemy import desc
import json

@bp.route('/activity-logs')
@login_required
@admin_required
def activity_logs():
    page = request.args.get('page', 1, type=int)
    
    # Filtres
    action = request.args.get('action', '')
    entity_type = request.args.get('entity_type', '')
    user_id = request.args.get('user_id', '')
    
    # Construire la requête
    query = ActivityLog.query
    
    if action:
        query = query.filter(ActivityLog.action == action)
    if entity_type:
        query = query.filter(ActivityLog.entity_type == entity_type)
    if user_id and user_id.isdigit():
        query = query.filter(ActivityLog.user_id == int(user_id))
    
    # Récupérer les logs paginés
    logs = query.order_by(desc(ActivityLog.timestamp)).paginate(page=page, per_page=20)
    
    # Récupérer les utilisateurs pour le filtre
    users = User.query.all()
    
    # Types d'entités et actions pour les filtres
    entity_types = ['WasteRecord', 'WasteType', 'Producer', 'Transporter', 
                   'TreatmentOperation', 'EliminationOperation']
    actions = ['create', 'update', 'delete']
    
    return render_template('main/activity_logs.html', 
                          title='Journal d\'activité',
                          logs=logs,
                          users=users,
                          entity_types=entity_types,
                          actions=actions,
                          parse_json=json.loads)

@bp.route('/activity-logs/<int:id>')
@login_required
@admin_required
def activity_log_details(id):
    log = ActivityLog.query.get_or_404(id)
    details = json.loads(log.details) if log.details else None
    
    return render_template('main/activity_log_details.html',
                          title='Détails de l\'activité',
                          log=log,
                          details=details)
