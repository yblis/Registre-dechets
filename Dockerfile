FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/home/appuser/.local/bin:$PATH"

# Create a non-root user
RUN useradd --create-home appuser

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
        curl \
        postgresql-client \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory and change ownership
WORKDIR /app
RUN chown appuser:appuser /app

# Switch to non-root user
USER appuser

# Install Python dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code and data
COPY --chown=appuser:appuser . .

# Ensure CSV files and scripts are present
RUN mkdir -p /app/scripts /app/app/utils/export_templates

# Copy CSV templates and init script
COPY --chown=appuser:appuser app/utils/export_templates/*.csv /app/app/utils/export_templates/
COPY --chown=appuser:appuser scripts/init_data.py /app/scripts/

# Ensure all files are executable
RUN chmod -R +x /app/scripts

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
