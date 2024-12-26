.PHONY: test test-verbose clean

test:
	PYTHONPATH=. python -m pytest

test-verbose:
	PYTHONPATH=. python -m pytest -v

test-coverage:
	PYTHONPATH=. python -m pytest --cov=. --cov-report=term-missing

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete 