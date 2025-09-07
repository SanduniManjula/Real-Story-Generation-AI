install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

lint:
	flake8 . && black --check .

test:
	pytest -q

run-api:
	uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload

run-ui:
	streamlit run app/streamlit_app.py

docker-build:
	docker build -t story-rt:latest .

docker-run:
	docker run --env-file .env -p 8000:8000 story-rt:latest
