import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('ENV.DATABASE_URL')
client = MongoClient(uri)
db = client.flask_db
