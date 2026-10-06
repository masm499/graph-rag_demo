import os
import csv
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


def create_healthcare_provider_node(provider, bio):

    create_provider_query = """
    MERGE (p:HealthcareProvider {name: $provider, bio: $bio})
    """
    # Query parameters, that indicate the provider value in the query is coming from provider parameter in function signature
    query_parameters = {"provider": provider, "bio": bio}

    try:
        driver.execute_query(
            create_provider_query,
            parameters_=query_parameters,
            database_=NEO4J_DATABASE,
        )
    except DriverError as e:
        print(f"Error creating HealthcareProvider node: {e}")


def create_patient_node(patient, patient_age, patient_gender, patient_condition):
    create_patient_query = """
    MERGE (p:Patient {name: $patient, age: $age, gender: $gender, condition: $condition})
    """
    query_parameters = {
        "patient": patient,
        "age": patient_age,
        "gender": patient_gender,
        "condition": patient_condition,
    }
    try:
        driver.execute_query(
            create_patient_query, parameters_=query_parameters, database_=NEO4J_DATABASE
        )
    except DriverError as e:
        print(f"Error creating Patient node: {e}")


def create_specialization_node(specialization):
    create_specialization_query = """
    MERGE (s:Specialization {name: $specialization})
    """
    query_parameters = {"specialization": specialization}
    try:
        driver.execute_query(
            create_specialization_query,
            parameters_=query_parameters,
            database_=NEO4J_DATABASE,
        )
    except DriverError as e:
        print(f"Error creating Specialization node: {e}")


def create_location_node(location):
    create_location_query = """
    MERGE (l:Location {name: $location})
    """
    query_parameters = {"location": location}

    try:
        driver.execute_query(
            create_location_query,
            parameters_=query_parameters,
            database_=NEO4J_DATABASE,
        )
    except DriverError as e:
        print(f"Error creating Location node: {e}")


def create_relationship(provider, patient, location, specialization):
    create_relationship_query = """
    MATCH (hcp:HealthcareProvider {name: $provider})
    MATCH (pt:Patient {name: $patient})
    MATCH (l:Location {name: $location})
    MATCH (s:Specialization {name: $specialization})
    MERGE (hcp)-[:TREATS]->(pt)
    MERGE (hcp)-[:LOCATED_IN]->(l)
    MERGE (hcp)-[:HAS_SPECIALIZATION]->(s)
    """
    query_parameters = {
        "provider": provider,
        "patient": patient,
        "location": location,
        "specialization": specialization,
    }
    try:
        driver.execute_query(
            create_relationship_query,
            parameters_=query_parameters,
            database_=NEO4J_DATABASE,
        )
    except DriverError as e:
        print(f"Error creating relationships: {e}")


if __name__ == "__main__":

    # 1. Get the absolute directory of the currently running script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    # 2. Combine that directory with your CSV filename
    CSV_PATH = os.path.join(SCRIPT_DIR, "healthcare.csv")

    with open(CSV_PATH, "r") as file:

        csv_reader = csv.DictReader(file)

        for row in csv_reader:

            provider = row["Provider"]
            bio = row["Bio"]
            patient = row["Patient"]
            age = row["Patient_Age"]
            gender = row["Patient_Gender"]
            condition = row["Patient_Condition"]
            location = row["Location"]
            specialization = row["Specialization"]

            create_healthcare_provider_node(provider, bio)
            create_patient_node(patient, age, gender, condition)
            create_specialization_node(specialization)
            create_location_node(location)
            create_relationship(provider, patient, location, specialization)

    print("Healthcare knowledge graph created successfully!")
