# Registre de Déchets

Application de gestion de registre de déchets avec support pour plusieurs types de déchets par enregistrement.

## Fonctionnalités

- Gestion des enregistrements de déchets
- Support pour plusieurs types de déchets par enregistrement
- Gestion des producteurs, transporteurs et opérations
- Export CSV des données
- Interface responsive (PWA)
- Authentification et gestion des utilisateurs

## Déploiement en Production

### Prérequis

- Docker et Docker Compose
- Traefik (pour le reverse proxy et SSL)

### Configuration

1. Cloner le dépôt:
   ```bash
   git clone https://github.com/yblis/Registre-dechets
   cd registre-dechets
   ```

2. Configurer les variables d'environnement:
   ```bash
   cp .env.example .env
   ```
   
   Modifier le fichier `.env` avec vos propres valeurs:
   - `SECRET_KEY`: Clé secrète pour Flask
   - `DB_PASSWORD`: Mot de passe pour la base de données
   - `DOMAIN`: Nom de domaine de l'application

3. Démarrer l'application:
   ```bash
   # Construire et démarrer les conteneurs
   docker-compose up -d --build
   
   # Suivre les logs d'initialisation (facultatif)
   docker-compose logs -f
   ```

   Le processus d'initialisation automatique:
   1. Attend que PostgreSQL soit prêt (vérification avec pg_isready)
   2. Exécute les migrations de la base de données
   3. Vérifie si un administrateur existe
   4. Crée l'administrateur si nécessaire avec les identifiants suivants:
      - Username: `${ADMIN_USERNAME:-admin}`
      - Email: `${ADMIN_EMAIL:-admin@example.com}`
      - Password: `${ADMIN_PASSWORD:-admin123}`
      
   Ces valeurs peuvent être configurées dans le fichier `.env`

   Une fois l'initialisation terminée, l'application est accessible sur:
   - URL: http://localhost:8000 (ou votre domaine configuré)
   - Connexion avec les identifiants admin définis ci-dessus

### Intégration avec Traefik

Pour utiliser Traefik comme reverse proxy, assurez-vous que votre configuration Traefik inclut:

```yaml
# traefik.yml
providers:
  docker:
    exposedByDefault: false

# Autres configurations Traefik...
```

L'application est déjà configurée avec les labels Traefik appropriés dans le fichier `docker-compose.yml`.

## Développement

### Installation locale

1. Créer un environnement virtuel:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

2. Installer les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurer les variables d'environnement:
   ```bash
   cp .env.example .env
   ```

4. Initialiser la base de données:
   ```bash
   flask db upgrade
   ```

5. Démarrer l'application:
   ```bash
   flask run
   ```

## Maintenance

### Sauvegardes

Pour sauvegarder la base de données:

```bash
docker-compose exec db pg_dump -U postgres waste_registry > backup.sql
```

### Mises à jour

Pour mettre à jour l'application:

```bash
git pull
docker-compose build
docker-compose up -d
docker-compose exec web flask db upgrade
```

## Dépannage

### Problèmes courants

1. L'application ne démarre pas:
   ```bash
   # Vérifier les logs des conteneurs
   docker-compose logs -f
   
   # Reconstruire l'image sans cache
   docker-compose build --no-cache web
   docker-compose up -d
   ```

2. La base de données n'est pas initialisée:
   ```bash
   # Vérifier les logs de la base de données
   docker-compose logs db
   
   # En cas de problème, réinitialiser les volumes
   docker-compose down -v
   docker-compose up -d
   ```

3. L'utilisateur admin n'est pas créé:
   ```bash
   # Vérifier les variables d'environnement
   docker-compose exec web env | grep ADMIN
   
   # Créer manuellement l'admin si nécessaire
   docker-compose exec web python3 -c "
   from app import create_app, db
   from app.models import User
   app = create_app()
   with app.app_context():
       if not User.query.filter_by(is_admin=True).first():
           admin = User(username='admin', email='admin@example.com', is_admin=True, active=True)
           admin.set_password('admin123')
           db.session.add(admin)
           db.session.commit()
           print('Admin créé avec succès')
   "
   ```

4. Erreurs de permissions:
   ```bash
   # Vérifier les permissions des volumes
   sudo chown -R 999:999 ./db-data  # Pour PostgreSQL
   sudo chown -R 1000:1000 ./app-data  # Pour l'application
   ```

## Licence

Ce projet est sous licence [MIT](LICENSE).
