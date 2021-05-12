# target: run - Run server
run:
	echo "Create database folder"
	[ -d data ] || mkdir data
	echo "Run develop server"
	uvicorn src.main:app --reload

# target: linter - Run linters
linter:
	flake8 . --count
	mypy .

# target: qa - Run test
qa:
	py.test
