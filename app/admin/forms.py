from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from app.models import User

class UserCreateForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Administrateur')
    submit = SubmitField('Créer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cet email est déjà utilisé.')

class UserEditForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    active = BooleanField('Compte actif')
    is_admin = BooleanField('Administrateur')
    new_password = PasswordField('Nouveau mot de passe (laisser vide pour ne pas changer)')
    submit = SubmitField('Enregistrer')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Cet email est déjà utilisé.')
