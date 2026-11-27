# Cairn backend

The backend is a FastAPI service. From this directory, create and activate a
virtual environment, install the development dependencies, and start the API:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

The interactive API documentation is available at
[`http://localhost:8000/docs`](http://localhost:8000/docs), and
[`http://localhost:8000/health`](http://localhost:8000/health) returns the
service health status.

Run the backend tests with:

```bash
pytest
```
