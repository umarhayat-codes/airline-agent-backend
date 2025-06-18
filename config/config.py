# from pymongo import MongoClient

# from dotenv import load_dotenv

# from os import getenv

# load_dotenv()
# def get_mongo_collection():
#     try:
#         url = getenv("MONGO_URL")
#         db_name = getenv("MONGO_DATABASE")
#         collection_name = getenv("MONGO_COLLECTION")
#         client = MongoClient(url)
#         db = client[db_name]
#         collection = db[collection_name]
#         return collection
#     except Exception as e:
#         print(f"Error occur during connect mongo: {e}")
#         return None


from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_mongo_collection():
    try: 
        url = getenv("MONGO_URL")
        db_name = getenv("MONGO_DATABASE")
        collection_name = getenv("MONGO_COLLECTION")
        client = MongoClient(url)
        db = client[db_name]
        collection = db[collection_name]
        return collection
    except Exception as e:
        print(f"Error occur during connect mongodb: {e}")
        return None
    


def get_mongo_db_user():
    try: 
        url = getenv("MONGO_URL")
        db_name = getenv("MONGO_DATABASE_USER")
        collection_name = getenv("MONGO_COLLECTION_USER")
        client = MongoClient(url)
        db = client[db_name]
        collection = db[collection_name]
        return collection
    except Exception as e:
        print(f"Error occur during connect mongodb: {e}")
        return None
    
    