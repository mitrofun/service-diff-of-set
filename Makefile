# target: run - Run server
run:
	uvicorn src.main:app --reload

# target: qa - Run test
qa:
	py.test
