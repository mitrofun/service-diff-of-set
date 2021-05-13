# target: migration - Run migration
migration:
	[ -d data ] || mkdir data
	alembic upgrade head

# target: run - Run server
run:
	echo "Run develop server"
	uvicorn src.main:app --reload

# target: linter - Run linters
linter:
	flake8 . --count
	mypy .

# target: qa - Run test
qa:
	py.test
