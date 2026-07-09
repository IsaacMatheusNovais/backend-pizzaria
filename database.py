import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def conectar():
    return psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST")
    )