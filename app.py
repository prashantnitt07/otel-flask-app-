from flask import Flask, request, jsonify
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource
from prometheus_client import start_http_server

# Initialize Flask app
app = Flask(__name__)

# OTEL Meter setup
resource = Resource.create({"service.name": "otel-flask-api"})
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Define metrics
request_counter = meter.create_counter(
    "flask_request_total", unit="1", description="Total number of HTTP requests"
)

response_time_histogram = meter.create_histogram(
    "flask_response_time_ms",
    unit="ms",
    description="Response time for Flask endpoints",
)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = (time.time() - request.start_time) * 1000
    request_counter.add(1, {"method": request.method, "endpoint": request.path})
    response_time_histogram.record(duration, {"method": request.method, "endpoint": request.path})
    return response

@app.route("/")
def home():
    return jsonify({"message": "Welcome to OTEL Flask API"})

@app.route("/api/data")
def data():
    time.sleep(0.5)
    return jsonify({"data": "Telemetry metrics in action!"})

if __name__ == "__main__":
    # Prometheus metrics exposed at :9464/metrics
    start_http_server(9464)
    app.run(host="0.0.0.0", port=7000)
