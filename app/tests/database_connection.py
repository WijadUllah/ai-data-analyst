
from app.db.connection import test_connection


try:
    if test_connection():
        print("PostgreSQL connection successful!")
except Exception as error:
    print("PostgreSQL connection failed.")
    print("Error type:", type(error).__name__)
    print("Check your database settings and PostgreSQL service.")
