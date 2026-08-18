build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker-compose exec bot uv run alembic -c alembic.ini upgrade head

migration:
	docker-compose exec bot uv run alembic -c alembic.ini revision --autogenerate -m "$(name)"

lint:
	uv run ruff check .

format:
	uv run ruff format .