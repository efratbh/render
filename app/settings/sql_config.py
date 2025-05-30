#set all our setting such as variabls and connection to the SQL
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

SQL_URL = os.getenv('NEON')

# 'postgresql://postgres:tuuytr@localhost:5432/students_db'