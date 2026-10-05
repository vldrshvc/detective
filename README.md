# Detective

A self-hosted service that watches web pages for you. Give it a link and tell it what to look for — a price dropping below a threshold, a new listing appearing — and it checks on a schedule and lets you know when something changes.

Think PriceSpy, but for any page and any condition.

## Status

Early stage. The REST API for managing **watchers** is working and backed by PostgreSQL.

A watcher is one thing you want tracked: a name, the URL to check, how often to check it, and whether it is currently active. Fetching and parsing pages is the next milestone.

## Stack

Python · FastAPI · SQLAlchemy 2.0 · PostgreSQL · uv

## Run locally

### Requirements

- Python 3.14
- PostgreSQL 17
- [uv](https://docs.astral.sh/uv/)

### Steps

Clone and install dependencies:

```bash
git clone git@github.com:vldrshvc/detective.git
cd detective
uv sync
```

Create the database:

```bash
createdb detective
```

Create a `.env` file in the project root:

DATABASE_URL=postgresql+psycopg://<your-postgres-user>@localhost/detective

Start the server:

```bash
uv run fastapi dev main.py
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs. Tables are created automatically on first start.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/watchers` | Create a watcher |
| `GET` | `/watchers` | List all watchers |
| `GET` | `/watchers/{id}` | Get one watcher, `404` if not found |
| `PUT` | `/watchers/{id}` | Replace a watcher's fields |
| `DELETE` | `/watchers/{id}` | Delete a watcher, returns `204` |

Example request body for `POST` and `PUT`:

```json
{
  "name": "Lenovo Legion 5",
  "url": "https://www.donedeal.ie/...",
  "interval_minutes": 60,
  "is_active": true
}
```

`interval_minutes` defaults to `60` and `is_active` to `true` if omitted.

## Roadmap

- [ ] Fetch a watcher's page and extract a value
- [ ] Run checks on a schedule
- [ ] Store check history
- [ ] Tests with pytest
- [ ] Docker setup
- [ ] Telegram notifications