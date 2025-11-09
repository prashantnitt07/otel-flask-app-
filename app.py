from flask import Flask, jsonify
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource

# Create OTEL resource
resource = Resource.create({"service.name": "otel-flask-app"})

# Prometheus exporter automatically serves /metrics on port 9464
prometheus_reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
metrics.set_meter_provider(provider)

# Create meter and counter
meter = metrics.get_meter("flask_app_meter")
request_counter = meter.create_counter(
    "flask_app_requests_total", description="Total requests to Flask app"
)

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    request_counter.add(1)
    return jsonify({"message": "Hello from OTEL Flask with Prometheus!"})
