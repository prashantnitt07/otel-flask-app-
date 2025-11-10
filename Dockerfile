FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 7000 9464
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn_config.py"]
