from flask import Flask, jsonify
import time

# OpenTelemetry imports
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# --- Setup OTEL MeterProvider with Prometheus exporter ---
prometheus_reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[prometheus_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Define metrics
request_counter = meter.create_counter(
    name="flask_http_requests_total",
    description="Number of HTTP requests processed",
    unit="1",
)

request_latency = meter.create_histogram(
    name="flask_http_request_duration_seconds",
    description="Duration of HTTP requests",
    unit="s",
)

# --- Flask App ---
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def index():
    start_time = time.time()

    # Simulate work
    time.sleep(0.02)

    duration = time.time() - start_time
    request_counter.add(1, {"endpoint": "/"})
    request_latency.record(duration, {"endpoint": "/"})

    return jsonify({"message": "Hello from OTEL Flask!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
