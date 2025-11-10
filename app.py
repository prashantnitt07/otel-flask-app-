from flask import Flask, jsonify
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import Counter, Histogram

# Create Flask app
app = Flask(__name__)

# Configure OTEL Metrics
resource = Resource.create({"service.name": "flask-otel-app"})

# ✅ Prometheus exporter on 0.0.0.0:9464
reader = PrometheusMetricReader(host="0.0.0.0", port=9464)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("flask_otel_metrics")

# Metrics: total requests and response time
request_counter = meter.create_counter(
    "flask_requests_total",
    description="Total number of requests received"
)

response_histogram = meter.create_histogram(
    "flask_response_duration_seconds",
    description="Response duration in seconds"
)


@app.route("/")
def home():
    start = time.time()
    request_counter.add(1, {"endpoint": "/"})
    time.sleep(0.2)  # simulate work
    duration = time.time() - start
    response_histogram.record(duration, {"endpoint": "/"})
    return jsonify({"message": "Welcome to Flask OTEL App"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
