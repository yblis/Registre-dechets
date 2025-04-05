#!/bin/bash
set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Running database migrations..."
flask db upgrade

echo "Creating admin user..."
flask create-admin-env

echo "Database initialization complete!"
