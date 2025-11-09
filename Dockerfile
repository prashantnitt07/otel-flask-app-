FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose app port and Prometheus metrics port
EXPOSE 7000
EXPOSE 9464

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "wsgi:application", "--workers", "2"]
