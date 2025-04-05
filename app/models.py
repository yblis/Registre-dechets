from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True, server_default='1')
    records = db.relationship('WasteRecord', backref='author', lazy='dynamic')
    logs = db.relationship('ActivityLog', backref='user', lazy='dynamic')

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def is_active(self):
        return self.active

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class WasteEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waste_record_id = db.Column(db.Integer, db.ForeignKey('waste_record.id'), nullable=False)
    waste_type_id = db.Column(db.Integer, db.ForeignKey('waste_type.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    
    # Relations
    waste_type_ref = db.relationship('WasteType', backref='entries')
    
    def __repr__(self):
        return f'<WasteEntry {self.waste_type_ref.code} - {self.quantity} {self.unit}>'

class WasteRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    transporter_id = db.Column(db.Integer, db.ForeignKey('transporter.id'), nullable=False)
    treatment_operation_id = db.Column(db.Integer, db.ForeignKey('treatment_operation.id'), nullable=False)
    elimination_operation_id = db.Column(db.Integer, db.ForeignKey('elimination_operation.id'), nullable=True)
    tracking_number = db.Column(db.String(64), unique=True, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relations
    waste_entries = db.relationship('WasteEntry', backref='record', lazy='dynamic', cascade='all, delete-orphan')
    producer_ref = db.relationship('Producer', backref='records')
    transporter_ref = db.relationship('Transporter', backref='records')
    treatment_operation_ref = db.relationship('TreatmentOperation', backref='records')
    elimination_operation_ref = db.relationship('EliminationOperation', backref='records')

    def __repr__(self):
        return f'<WasteRecord {self.tracking_number}>'

class WasteType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(128), nullable=False)
    dangerous = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<WasteType {self.code}>'

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    siret = db.Column(db.String(14), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Producer {self.name}>'

class Transporter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    siret = db.Column(db.String(14), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    registration = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<Transporter {self.name}>'

class TreatmentOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<TreatmentOperation {self.code}>'

class EliminationOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<EliminationOperation {self.code}>'

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(20), nullable=False)  # 'create', 'update', 'delete'
    entity_type = db.Column(db.String(50), nullable=False)  # 'WasteRecord', 'Producer', etc.
    entity_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=True)  # JSON or description of changes

    def __repr__(self):
        return f'<ActivityLog {self.action} {self.entity_type} {self.entity_id}>'
