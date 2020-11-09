POSTGRES_USER ?= $(POSTGRES_USER)
QUERY ?= SELECT * FROM stores;

query-command=(docker exec -it instacart-postgres psql -U $(POSTGRES_USER) -c $1)

.PHONY: build
build:
	docker-compose build

start-database:
	docker-compose up -d database

wait-database:
	docker-compose run --rm --no-deps --entrypoint "wait-for-it --timeout=30 database:5432" instacart

.PHONY: database
database: start-database wait-database

.PHONY: run
run: build database
	docker-compose run --rm --no-deps instacart

.PHONY: sql
sql:
	docker exec -it instacart-postgres psql -U $(POSTGRES_USER)

sql-query:
	$(call query-command, "$(QUERY)")

sql-select-all:
	$(call query-command, "SELECT * FROM stores")
	$(call query-command, "SELECT * FROM shelves")
	$(call query-command, "SELECT * FROM shelf_items")

destroy:
	docker-compose down -v --rmi all

dev-setup:
	pip install -r requirements/dev.txt
	pre-commit install
