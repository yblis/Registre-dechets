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

# Copy application code
COPY --chown=appuser:appuser . .

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
