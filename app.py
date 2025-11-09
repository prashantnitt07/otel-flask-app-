from flask import Flask, jsonify
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource
import time

# OpenTelemetry setup
resource = Resource.create({"service.name": "otel-flask-app"})
prometheus_reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("flask_app_meter")
request_counter = meter.create_counter("flask_app_requests_total")

# Flask setup
app = Flask(__name__)

@app.route("/")
def home():
    request_counter.add(1)
    return jsonify({"message": "Hello from OTEL Flask!"})

@app.route("/metrics")
def metrics_endpoint():
    return prometheus_reader.render_metrics()
