import os

from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')


def mongo_connection():
    client = MongoClient(MONGO_URI)
    db = client['inventario_db']
    return db['funcionarios']
