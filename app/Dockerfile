FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  python3-psycopg2 \
  && apt-get clean


COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app

WORKDIR /app

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
