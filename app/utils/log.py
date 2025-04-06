from flask_login import current_user
from app.models import ActivityLog
from app import db
import json

def log_activity(action: str, entity_type: str, entity_id: int, details: dict = None):
    """Log une activité dans la base de données."""
    activity = ActivityLog(
        user_id=current_user.id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=json.dumps(details) if details else None
    )
    db.session.add(activity)
    db.session.commit()
