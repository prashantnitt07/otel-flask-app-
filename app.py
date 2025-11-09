from flask import Flask, jsonify
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource

import time

app = Flask(__name__)

# ---- OTEL Prometheus Exporter ----
resource = Resource(attributes={"service.name": "otel-flask-app"})

# Create a Prometheus Metric Reader
prometheus_reader = PrometheusMetricReader(port=9464, host="0.0.0.0")

# Create the Meter Provider with Prometheus reader
provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("flask_app_meter")

# ---- Example metrics ----
request_counter = meter.create_counter(
    name="flask_app_requests_total",
    description="Total number of requests received",
)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
