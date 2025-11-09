# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose only Flask app port (metrics also served here)
EXPOSE 7000

# Start Gunicorn with Flask app (defined in wsgi.py)
CMD ["gunicorn", "--bind", "0.0.0.0:7000", "wsgi:application", "--workers", "2"]
