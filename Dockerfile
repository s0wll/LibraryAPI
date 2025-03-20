FROM python:3.12.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD sleep 5; alembic upgrade head; python src/main.py