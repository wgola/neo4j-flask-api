from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from neo4j.exceptions import AuthError


def connectDB():
    load_dotenv()
    uri = os.getenv("NEO_URI")
    user = os.getenv("NEO_USER")
    password = os.getenv("NEO_PASSWORD")

    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        driver.verify_connectivity()
    except AuthError:
        print("Couldn't connect to DB: wrong authorization")
        return None
    except ValueError:
        print("Couldn't connect to DB: wrong address")
        return None
    
    
    print("Connected to DB")
    return driver
