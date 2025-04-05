#!/bin/bash
set -e

echo "Waiting for database to be ready..."
for i in {1..30}; do
    if flask db current > /dev/null 2>&1; then
        echo "Database is ready"
        break
    fi
    echo "Waiting for database... ($i/30)"
    sleep 2
done

# Run migrations if needed
echo "Running database migrations..."
flask db upgrade

# Check if admin user exists
echo "Checking admin user..."
if ! flask shell <<EOF
from app.models import User
admin = User.query.filter_by(is_admin=True).first()
exit(0 if admin else 1)
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
