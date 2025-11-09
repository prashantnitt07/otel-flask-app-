from app import app, prometheus_reader
from opentelemetry.exporter.prometheus import start_http_server

# The Prometheus exporter opens its own HTTP endpoint.
# Prometheus scrapes this endpoint, not Flask's 7000.
METRICS_PORT = 9464
start_http_server(port=METRICS_PORT)

application = app
