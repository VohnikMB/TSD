import xml.etree.ElementTree
import random
import mysql.connector
from datetime import datetime
import time

db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "animal_shelter"
    }
def measure_query_time():
    query = "SELECT * FROM animal"
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        start_time = time.time()
        cursor.execute(query)
        cursor.fetchall()  # Отримати результати запиту
        end_time = time.time()
        execution_time = end_time - start_time
        print("Час виконання запиту: {:.6f} секунд".format(execution_time))
        return execution_time
    finally:
        cursor.close()
        connection.close()

def date(age):
    local_dt = datetime.now()
    date_of_birth = local_dt.year - age
    date_of_birth_month = random.randint(1, 12)
    date_of_birth_day = random.randint(1, 28)
    date_of_birth_reth = f"{date_of_birth}-{date_of_birth_month:02d}-{date_of_birth_day:02d}"
    date_of_arrival_reth = f"{random.randint(date_of_birth, local_dt.year)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    return date_of_birth_reth, date_of_arrival_reth

def get_random_xml():
    xml_file_path = ("BLL\\DATAIN\\animal.xml")
    tree = xml.etree.ElementTree.parse(xml_file_path)
    root = tree.getroot()
    names = root.find('name')
    species = root.find('species')
    status = root.find('status')
    random_name = random.choice([name.text for name in names.findall('value')])
    random_species = random.choice([s.text for s in species.findall('value')])
    random_status = random.choice([st.text for st in status.findall('value')])

    return random_name, random_species, random_status

def max_ID():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        query = "SELECT MAX(animal_id) FROM animal"
        cursor.execute(query)
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 1
    finally:
        cursor.close()
        connection.close()

def register_new_animal(number):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    start_time = time.time()
    try:
        user_query = "INSERT INTO animal (animal_id, name, species, age, date_of_birth, arrival_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        for i in range(int(number)):
            random_name, random_species, random_status = get_random_xml()
            age = random.randint(1, 20)
            date_of_birth, date_of_arrival = date(age)
            user_values = (max_ID(), random_name, random_species, age, date_of_birth, date_of_arrival, random_status)
            cursor.execute(user_query, user_values)
            connection.commit()
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        print("Час виконання запиту: {:.6f} секунд".format(execution_time))
        cursor.close()
        connection.close()