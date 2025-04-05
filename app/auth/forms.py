from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur ou Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Répéter le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class UpdateAccountForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    current_password = PasswordField('Mot de passe actuel')
    new_password = PasswordField('Nouveau mot de passe')
    confirm_password = PasswordField('Confirmer le mot de passe', 
        validators=[EqualTo('new_password', message='Les mots de passe doivent correspondre')])
    submit = SubmitField('Mettre à jour')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Cette adresse email est déjà utilisée.')

    def validate_current_password(self, field):
        if self.new_password.data and not field.data:
            raise ValidationError('Vous devez fournir votre mot de passe actuel pour le changer.')
