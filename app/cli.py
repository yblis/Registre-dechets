import click
import os
from flask.cli import with_appcontext
from app import db
from app.models import User

def register_commands(app):
    app.cli.add_command(create_admin)
    app.cli.add_command(create_admin_env)
    app.cli.add_command(promote_admin)

@click.command('create-admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(username, email, password):
    """Créer un nouvel utilisateur administrateur avec des arguments."""
    _create_admin_user(username, email, password)

@click.command('create-admin-env')
@with_appcontext
def create_admin_env():
    """Créer un nouvel utilisateur administrateur à partir des variables d'environnement."""
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    _create_admin_user(username, email, password)

def _create_admin_user(username, email, password):
    """Fonction interne pour créer un administrateur."""
    if User.query.filter_by(username=username).first():
        click.echo(f'Erreur: L\'utilisateur {username} existe déjà.')
        return
    if User.query.filter_by(email=email).first():
        click.echo(f'Erreur: L\'email {email} est déjà utilisé.')
        return
    
    user = User(username=username, email=email, is_admin=True, active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'L\'administrateur {username} a été créé avec succès.')

@click.command('promote-admin')
@click.argument('username')
@with_appcontext
def promote_admin(username):
    """Promouvoir un utilisateur en administrateur."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        click.echo(f'Erreur: L\'utilisateur {username} n\'existe pas.')
        return

    if user.is_admin:
        click.echo(f'L\'utilisateur {username} est déjà administrateur.')
        return

    user.is_admin = True
    db.session.commit()
    click.echo(f'L\'utilisateur {username} est maintenant administrateur.')
