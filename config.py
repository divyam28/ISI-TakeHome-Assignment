import os

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
dbname = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

db_uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

