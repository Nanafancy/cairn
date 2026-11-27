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

The README's initial REST surface is registered: `GET /rounds`,
`GET /rounds/{round_id}`, `GET /rounds/{round_id}/projects`,
`GET /projects/{project_id}`, `POST /rounds/{round_id}/simulate`, and
`GET /donors/{address}/history`. The simulation request accepts project IDs,
contribution amounts, a matching pool, and an optional per-donor cap; it
returns the quadratic raw score and the normalized pool allocation.

Round, project, and donation reads currently return empty collections or 404
because the Soroban event indexer and database described in the root README
have not been implemented yet. The simulation endpoint works directly from
the supplied hypothetical data and does not submit transactions.

Run the backend tests with:

```bash
pytest
```
