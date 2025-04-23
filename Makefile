lint:
	python -m flake8 app
	python -m mypy app
	python -m isort -c --diff app
	python -m black --check --diff app

prettify:
	python -m isort app
	python -m black app