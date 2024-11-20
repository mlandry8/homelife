import os

conf = {
    "mongo": {
        "host": os.getenv("MONGO_HOST"),
        "port": os.getenv("MONGO_PORT"),
        "username": os.getenv("MONGO_USERNAME"),
        "password": os.getenv("MONGO_PASSWORD"),
        "database": os.getenv("MONGO_DB_NAME"),
    }
}
