from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.admin import bp
from app.admin.decorators import admin_required
from app.admin.forms import UserEditForm, UserCreateForm
from app.models import User

@bp.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            is_admin=form.is_admin.data,
            active=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'L\'utilisateur {user.username} a été créé avec succès.', 'success')
        return redirect(url_for('admin.users'))
    
    users = User.query.order_by(User.username).all()
    return render_template('admin/users.html', title='Gestion des utilisateurs', users=users, form=form)

@bp.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    
    # Empêcher l'admin de modifier son propre statut admin
    if user == current_user:
        flash('Vous ne pouvez pas modifier votre propre compte ici. Utilisez la page profil.', 'warning')
        return redirect(url_for('admin.users'))
    
    form = UserEditForm(user.username, user.email)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.active = form.active.data
        user.is_admin = form.is_admin.data
        
        if form.new_password.data:
            user.set_password(form.new_password.data)
        
        db.session.commit()
        flash(f'Les modifications pour l\'utilisateur {user.username} ont été enregistrées.', 'success')
        return redirect(url_for('admin.users'))
    
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.active.data = user.active
        form.is_admin.data = user.is_admin
    
    return render_template('admin/edit_user.html', title='Modifier utilisateur', form=form, user=user)

@bp.route('/user/<int:id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    
    # Empêcher la désactivation de son propre compte
    if user == current_user:
        flash('Vous ne pouvez pas désactiver votre propre compte.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.active = not user.active
    db.session.commit()
    
    status = 'activé' if user.active else 'désactivé'
    flash(f'Le compte de {user.username} a été {status}.', 'success')
    return redirect(url_for('admin.users'))
