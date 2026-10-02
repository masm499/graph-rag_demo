import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import DriverError

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)

def setup_neo4j_connection():

    try:
        driver.verify_connectivity();
        print("Connected to Neo4j successfully!");
    except DriverError as e:
        print("Error connecting to Neo4j:", e)

    
def create_entities(tx):

    # Domain/Scope : Scientists
    tx.run("MERGE (s:Person:Scientist {name: 'Albert Einstein'})")
    tx.run("MERGE (c:Country {name: 'Germany'})")
    tx.run("MERGE (c:Country {name: 'USA'})")
    tx.run("MERGE (s:Subject {name:'Physics'})")
    tx.run("MERGE (a:Awards {name:'Nobel Prize In Physics'})")

    create_relationships(tx, "Albert Einstein", "Germany", "BORN_IN")
    create_relationships(tx, "Albert Einstein", "USA", "DIED_IN")
    create_relationships(tx, "Albert Einstein", "Physics", "STUDIED")
    create_relationships(tx, "Albert Einstein", "Nobel Prize In Physics", "WON")


def create_relationships(tx, entity1, entity2, relationship_type):

    #Not using label will cause a huge search across all nodes, so its very inefficient
    tx.run(f"""
        MATCH (a {{name: '{entity1}'}}), (b {{name: '{entity2}'}})
        MERGE (a)-[r:{relationship_type}]->(b)
    """)


def query_graph(cypher_query):

    try:

        result = driver.execute_query(cypher_query, database_=NEO4J_DATABASE)

        print("Query Results:")

        for record in result[0]:
            print(record.get("name"))
    except Exception as e:
        print("Error connecting to Neo4j:", e)



def build_knowledge_graph():

    setup_neo4j_connection()

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            session.execute_write(create_entities)
    except DriverError as e:
        print("Error creating entities:", e)
    


if __name__ == "__main__":
    
     build_knowledge_graph()
     query_graph("MATCH (n) RETURN n.name AS name")
