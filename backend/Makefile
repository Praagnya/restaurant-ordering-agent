db-up:
	docker compose up -d

db-down:
	docker compose down

db-reset:
	docker compose down -v
	docker compose up -d

migrate:
	.venv/bin/alembic upgrade head

setup: db-up migrate

run:
	.venv/bin/uvicorn app.api.app:app --reload --port 8000

test:
	.venv/bin/pytest tests/
