# Multiple Models Serving with Ray[serve]

Serve multiple models along an existing FastAPI app:

* One-off vectoriser and reranker models
* Composite model that invokes other models

Can also be deployed separately with a config file.

## Local setup

Run with Docker:

```bash
docker build -t mserve:latest .
docker run -p 8080:8080 -p 3000:3000 mserve:latest
```

Or in a Python environment:

```bash
# Install Python 3.11, create virtual environment and source in it, then:
pip install -r requirements.txt
uvicorn src.entrypoint:app --host 0.0.0.0 --port 8080
```

## Performance tests

Run performance tests with:

```bash
# Given that you're in a virtual environment with installed requirements:
locust -f tests/locustfile.py
```

## Example usage

Reranker:

```bash
curl -X POST http://localhost:8080/rerank -H "content-type: application/json" -d '{"pair": ["What is Python?", "Python is the best programming language"]}'
```

Vectoriser:

```bash
curl -X POST http://localhost:8080/vectorise -H "content-type: application/json" -d '{"text": "Vectorise this text"}'
```

Composite:

```bash
curl -X POST http://localhost:8080/composite -H "content-type: application/json" -d '{"text": "Compose this text"}'
```