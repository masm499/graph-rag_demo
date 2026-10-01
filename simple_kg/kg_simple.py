import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

try:

    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)

    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("MATCH (n) RETURN n LIMIT 5")
        for record in result:
            print(record)

except Exception as e:
    print("Error connecting to Neo4j:", e)
finally:
    driver.close()
