#!/usr/bin/python3
"""This module instantiates the storage based on the environment variable """
from os import getenv

"""
environ["HBNB_MYSQL_USER"] = "hbnb_dev"
environ["HBNB_MYSQL_PWD"] = "hbnb_dev_pwd"
environ["HBNB_MYSQL_HOST"] = "localhost"
environ["HBNB_MYSQL_DB"] = "hbnb_dev_db"
environ["HBNB_TYPE_STORAGE"] = "db"
"""

storage_env = getenv('HBNB_TYPE_STORAGE')

if storage_env == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Reload the storage
storage.reload()
