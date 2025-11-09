from flask import Flask, jsonify
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource
import time

# -----------------------------
# OpenTelemetry Prometheus setup
# -----------------------------
resource = Resource.create({"service.name": "otel-flask-app"})

# Create Prometheus reader (no host/port args)
prometheus_reader = PrometheusMetricReader()

provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("flask_app_meter")

# Define a simple counter
request_counter = meter.create_counter(
    "flask_app_requests_total",
    description="Total number of requests received",
)

# -----------------------------
# Flask application
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    request_counter.add(1)
    return jsonify({"message": "Hello from OTEL Flask!"})

@app.route("/work")
def work():
    start = time.time()
    time.sleep(0.3)
    duration = time.time() - start
    return jsonify({"work_duration": duration})

# -----------------------------
# Expose metrics via Prometheus endpoint
# -----------------------------
@app.route("/metrics")
def metrics_endpoint():
    return prometheus_reader.render_metrics()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
