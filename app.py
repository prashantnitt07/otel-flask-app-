from flask import Flask, jsonify
from opentelemetry import metrics
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

app = Flask(__name__)

# OTEL setup
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
set_meter_provider(provider)

meter = metrics.get_meter("flask-app")

request_counter = meter.create_counter(
    name="flask_request_count",
    description="Number of requests received",
)

@app.route("/")
def index():
    request_counter.add(1, {"endpoint": "/"})
    return jsonify({"message": "Welcome to OTEL Flask app!"})

@app.route("/vote")
def vote():
    request_counter.add(1, {"endpoint": "/vote"})
    return jsonify({"message": "Vote received!"})

# This exposes metrics automatically at /metrics (handled by OTEL exporter)
