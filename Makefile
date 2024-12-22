run:
	@cd src && python3 main.py

lint:
	@cd src && python3 -m ruff check . --fix

migrate-deps:
	@bash -c 'poetry export --without-hashes --format=requirements.txt > requirements.txt && git add requirements.txt'
