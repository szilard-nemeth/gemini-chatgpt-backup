test:
	nosetests tests

setup:
	pip install -r requirements.txt
	poetry install
	poetry run playwright install chromium
	npm install -g single-file-cli

run:
	poetry run python publix_export_playwright_structured.py
