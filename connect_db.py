import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ConfigurationError


def connect_db():
    load_dotenv()
    uri = os.getenv("NEO_URI")
    user = os.getenv("NEO_USER")
    password = os.getenv("NEO_PASSWORD")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
    except AuthError:
        print("Couldn't connect to DB: wrong authorization")
        return None
    except (ValueError, ConfigurationError):
        print("Couldn't connect to DB: wrong address")
        return None

    print("Connected to DB")
    return driver
