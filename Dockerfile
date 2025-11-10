FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 7000 9464
CMD ["gunicorn", "--bind", "0.0.0.0:7000", "app:app"]
