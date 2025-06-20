import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

SQL_URL = os.getenv('NEON')
