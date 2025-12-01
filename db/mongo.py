import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv() 


# initialize the connection to the database
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DATABASE_NAME")



def get_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    return db



TEST_DB_NAME = "booksdb_test"

def get_test_db():
    client = AsyncIOMotorClient(MONGO_URI)

    return client[TEST_DB_NAME]
