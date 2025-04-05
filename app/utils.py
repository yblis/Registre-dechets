import json
from flask_login import current_user
from app import db
from app.models import ActivityLog

def log_activity(action, entity_type, entity_id, details=None):
    """
    Enregistre une activité dans le journal d'activité.
    
    Args:
        action (str): Type d'action ('create', 'update', 'delete')
        entity_type (str): Type d'entité ('WasteRecord', 'Producer', etc.)
        entity_id (int): ID de l'entité concernée
        details (dict, optional): Détails supplémentaires sur l'action
    """
    if details and isinstance(details, dict):
        details = json.dumps(details)
    
    log = ActivityLog(
        user_id=current_user.id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    
    db.session.add(log)
    db.session.commit()
