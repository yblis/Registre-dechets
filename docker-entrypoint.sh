#!/bin/bash
set -e

echo "Waiting for database to be ready..."
export PGPASSWORD=${DB_PASSWORD}
until pg_isready -h db -U postgres; do
    echo "Waiting for database..."
    sleep 2
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
export FLASK_APP=run.py
if ! flask db upgrade; then
    echo "Error: Database migration failed!"
    exit 1
fi

# Check if admin user exists and create if needed
echo "Checking admin user..."
if ! flask shell <<EOF
from app.models import User
from app import db
admin = User.query.filter_by(is_admin=True).first()
if not admin:
    print("Creating admin user...")
    admin = User(
        username="${ADMIN_USERNAME:-admin}",
        email="${ADMIN_EMAIL:-admin@example.com}",
        is_admin=True,
        active=True
    )
    admin.set_password("${ADMIN_PASSWORD:-admin123}")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully")
else:
    print("Admin user already exists")
exit(0)
EOF
then
    echo "Creating admin user..."
    flask create-admin-env
else
    echo "Admin user already exists"
fi

# Start the application
echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app
