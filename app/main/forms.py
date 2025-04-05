from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, DateField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, Length
from app.models import WasteType, Producer, Transporter, TreatmentOperation, EliminationOperation

class WasteEntryForm(FlaskForm):
    waste_type_id = SelectField('Type de déchet', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantité', validators=[DataRequired()])
    unit = SelectField('Unité', validators=[DataRequired()], choices=[
        ('kg', 'Kilogrammes'),
        ('tons', 'Tonnes')
    ])
    treatment_operation_id = SelectField('Opération de traitement prévue', coerce=int, validators=[DataRequired()])
    elimination_operation_id = SelectField('Opération d\'élimination', validators=[Optional()], 
        coerce=lambda x: int(x) if x and x != 'None' else None)

    class Meta:
        csrf = False

    def __init__(self, *args, **kwargs):
        super(WasteEntryForm, self).__init__(*args, **kwargs)
        self.waste_type_id.choices = [(wt.id, f"{wt.code} - {wt.description}") 
                                    for wt in WasteType.query.order_by(WasteType.code).all()]
        self.treatment_operation_id.choices = [(op.id, f"{op.code} - {op.description}") 
                                            for op in TreatmentOperation.query.order_by(TreatmentOperation.code).all()]
        self.elimination_operation_id.choices = [('None', 'Aucune')] + [(op.id, f"{op.code} - {op.description}") 
                                              for op in EliminationOperation.query.order_by(EliminationOperation.code).all()]

class WasteRecordForm(FlaskForm):
    date = DateField('Date d\'entrée', validators=[DataRequired()])
    waste_entries = FieldList(FormField(WasteEntryForm), min_entries=1)
    producer_id = SelectField('Producteur', coerce=int, validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired(), Length(max=128)])
    transporter_id = SelectField('Transporteur', coerce=int, validators=[DataRequired()])
    tracking_number = StringField('N° Bordereau', validators=[DataRequired(), Length(max=64)])
    notes = TextAreaField('Remarques', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(WasteRecordForm, self).__init__(*args, **kwargs)
        self.producer_id.choices = [(p.id, f"{p.name} ({p.siret})") 
                                  for p in Producer.query.order_by(Producer.name).all()]
        self.transporter_id.choices = [(t.id, f"{t.name} ({t.registration})") 
                                     for t in Transporter.query.order_by(Transporter.name).all()]

class SearchForm(FlaskForm):
    start_date = DateField('Date de début', validators=[Optional()])
    end_date = DateField('Date de fin', validators=[Optional()])
    waste_type_id = SelectField('Type de déchet', validators=[Optional()], 
        choices=[('', 'Tous')], coerce=lambda x: int(x) if x else None)
    producer_id = SelectField('Producteur', validators=[Optional()], 
        choices=[('', 'Tous')], coerce=lambda x: int(x) if x else None)
    destination = StringField('Destination', validators=[Optional(), Length(max=128)])
    transporter_id = SelectField('Transporteur', validators=[Optional()], 
        choices=[('', 'Tous')], coerce=lambda x: int(x) if x else None)
    submit = SubmitField('Rechercher')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        try:
            self.waste_type_id.choices += [(wt.id, f"{wt.code} - {wt.description}") 
                                        for wt in WasteType.query.order_by(WasteType.code).all()]
            self.producer_id.choices += [(p.id, f"{p.name} ({p.siret})") 
                                      for p in Producer.query.order_by(Producer.name).all()]
            self.transporter_id.choices += [(t.id, f"{t.name} ({t.registration})") 
                                         for t in Transporter.query.order_by(Transporter.name).all()]
        except:
            pass  # Handle the case when tables don't exist yet
