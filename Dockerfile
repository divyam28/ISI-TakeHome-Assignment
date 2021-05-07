FROM python:3.7

LABEL Maintainer "Divyam Khanna"

RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV="docker"
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=isi

EXPOSE 5000
EXPOSE 5432


ENTRYPOINT ["python", "run.py"]