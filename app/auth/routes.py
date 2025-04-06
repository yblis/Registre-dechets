from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, UpdateAccountForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.username.data)
        ).first()
        if user is None or not user.check_password(form.password.data):
            flash('Identifiant ou mot de passe invalide', 'danger')
            return redirect(url_for('auth.login'))
        if not user.active:
            flash('Ce compte a été désactivé. Contactez un administrateur.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Connexion', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitations, vous êtes maintenant inscrit!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Inscription', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        
        # Si un nouveau mot de passe est fourni
        if form.new_password.data:
            if not current_user.check_password(form.current_password.data):
                flash('Mot de passe actuel incorrect.', 'danger')
                return redirect(url_for('auth.profile'))
            current_user.set_password(form.new_password.data)
        
        db.session.commit()
        flash('Votre profil a été mis à jour avec succès.', 'success')
        return redirect(url_for('auth.profile'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        
    return render_template('auth/profile.html', title='Profil', form=form)
