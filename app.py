from fastapi import FastAPI
import random
from prometheus_client import Counter, generate_latest, REGISTRY
from starlette.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total number of requests", ["endpoint"])

@app.get("/")
def read_root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {"message": "Hello, FastAPI!"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain")

@app.get("/random")
def random_number():
    REQUEST_COUNT.labels(endpoint="/random").inc()
    return {"random_number": random.randint(1, 100)}