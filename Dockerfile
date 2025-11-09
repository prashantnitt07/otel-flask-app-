FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7000
EXPOSE 9464  # for Prometheus scrape

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "wsgi:application", "--workers", "2"]
