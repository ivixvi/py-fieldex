.PHONY: format

format:
	- poetry run isort .
	- poetry run black py_fieldex
	- poetry run black tests
