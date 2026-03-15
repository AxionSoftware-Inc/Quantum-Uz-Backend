FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Django port
EXPOSE 8000

# We use gunicorn to serve applications dynamically and securely.
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
