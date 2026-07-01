# app/monitoring/metrics.py
from prometheus_client import Counter, Histogram, generate_latest

REQUESTS = Counter("requests_total", "Total requests")
ERRORS = Counter("errors_total", "Total errors")
LATENCY = Histogram("request_latency_seconds", "Request latency")

def track_request(func):
    def wrapper(*a, **k):
        REQUESTS.inc()
        with LATENCY.time():
            try:
                return func(*a, **k)
            except Exception:
                ERRORS.inc()
                raise
    return wrapper

def metrics_response():
    return generate_latest(), 200, {"Content-Type": "text/plain"}