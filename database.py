import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

print(os.getenv("DB_PASSWORD"))

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="pizzaria",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )