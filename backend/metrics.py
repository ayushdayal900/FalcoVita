from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

# Define HTTP requests count metric
HTTP_REQUEST_COUNT = Counter(
    "falcovita_http_requests_total",
    "Total HTTP requests count",
    ["method", "endpoint", "status_code"]
)

# Define HTTP request latency profile
HTTP_REQUEST_LATENCY = Histogram(
    "falcovita_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float("inf"))
)

def metrics_endpoint():
    """Returns Prometheus scraped text payload."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
