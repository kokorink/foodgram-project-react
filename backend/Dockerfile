FROM python:3.9

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py dataload

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]
