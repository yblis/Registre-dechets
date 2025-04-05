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
   docker-compose up -d
   ```

4. Initialiser la base de données:
   ```bash
   docker-compose exec web flask db upgrade
   ```

5. Créer un utilisateur administrateur:
   ```bash
   docker-compose exec web flask create-admin
   ```

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

## Licence

Ce projet est sous licence [MIT](LICENSE).
