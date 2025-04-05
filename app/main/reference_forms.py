from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import WasteType, Producer, Transporter, TreatmentOperation, EliminationOperation

class WasteTypeForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    dangerous = BooleanField('Déchet dangereux')
    submit = SubmitField('Enregistrer')

    def validate_code(self, code):
        waste_type = WasteType.query.filter_by(code=code.data).first()
        if waste_type and waste_type.id != getattr(self, '_obj_id', None):
            raise ValidationError('Ce code est déjà utilisé.')

class ProducerForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    siret = StringField('SIRET', validators=[DataRequired(), Length(min=14, max=14)])
    address = TextAreaField('Adresse', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

    def validate_siret(self, siret):
        producer = Producer.query.filter_by(siret=siret.data).first()
        if producer and producer.id != getattr(self, '_obj_id', None):
            raise ValidationError('Ce numéro SIRET est déjà utilisé.')

class TransporterForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    siret = StringField('SIRET', validators=[DataRequired(), Length(min=14, max=14)])
    address = TextAreaField('Adresse', validators=[DataRequired()])
    registration = StringField('Immatriculation', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Enregistrer')

    def validate_siret(self, siret):
        transporter = Transporter.query.filter_by(siret=siret.data).first()
        if transporter and transporter.id != getattr(self, '_obj_id', None):
            raise ValidationError('Ce numéro SIRET est déjà utilisé.')

class TreatmentOperationForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Enregistrer')

    def validate_code(self, code):
        operation = TreatmentOperation.query.filter_by(code=code.data).first()
        if operation and operation.id != getattr(self, '_obj_id', None):
            raise ValidationError('Ce code est déjà utilisé.')

class EliminationOperationForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Enregistrer')

    def validate_code(self, code):
        operation = EliminationOperation.query.filter_by(code=code.data).first()
        if operation and operation.id != getattr(self, '_obj_id', None):
            raise ValidationError('Ce code est déjà utilisé.')

class ImportForm(FlaskForm):
    file = FileField('Fichier CSV', validators=[FileRequired(), FileAllowed(['csv'], 'CSV uniquement!')])
    submit = SubmitField('Importer')
