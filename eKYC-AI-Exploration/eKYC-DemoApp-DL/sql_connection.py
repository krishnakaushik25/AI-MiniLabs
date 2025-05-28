import mysql.connector
import pandas as pd
import logging
import os 
import toml

# Logging configuration
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

# Load database configuration from config.toml
config = toml.load("config.toml")
db_config = config.get("database", {})

db_user = db_config.get("user")
db_password = db_config.get("password")
db_host = db_config.get("host", "localhost")
db_name = db_config.get("database")

if not db_user or not db_password:
    logging.error("Database user or password not found in config.toml")
    raise ValueError("Database user or password not found in config.toml")

# Establish a connection to the MySQL server
try:
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    mycursor = mydb.cursor()
    logging.info("Connection established with database")
except mysql.connector.Error as err:
    logging.error(f"Error connecting to the database: {err}")
    raise



def insert_records(text_info):
    try:
        sql = "INSERT INTO users(id, name, father_name, dob, id_type, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (text_info['ID'],
                  text_info['Name'],
                  text_info["Father's Name"],
                  text_info['DOB'],  # Make sure this is formatted as a string 'YYYY-MM-DD'
                  text_info['ID Type'],
                  str(text_info['Embedding']))
        
        mycursor.execute(sql, values)
        mydb.commit()
        logging.info("Inserted records successfully into users table.")
    except Exception as e:
        logging.error(f"Error inserting records into users table: {e}")

def insert_records_aadhar(text_info):
    try:
        sql = "INSERT INTO aadhar(id, name, gender, dob, id_type, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (text_info['ID'],
                  text_info['Name'],
                  text_info["Gender"],
                  text_info['DOB'],  # Make sure this is formatted as a string 'YYYY-MM-DD'
                  text_info['ID Type'],
                  str(text_info['Embedding']))
        
        mycursor.execute(sql, values)
        mydb.commit()
        logging.info("Inserted records successfully into aadhar table.")
    except Exception as e:
        logging.error(f"Error inserting records into aadhar table: {e}")

def fetch_records(text_info):
    try:
        sql = "SELECT * FROM users WHERE id = %s"
        values = (text_info['ID'],)
        mycursor.execute(sql, values)
        result = mycursor.fetchall()
        if result:
            df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
            logging.info("Fetched records successfully from users table.")
            return df
        else:
            logging.info("No records found.")
            return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error fetching records: {e}")
        return pd.DataFrame()
    
def fetch_records_aadhar(text_info):
    try:
        sql = "SELECT * FROM aadhar WHERE id = %s"
        values = (text_info['ID'],)
        mycursor.execute(sql, values)
        result = mycursor.fetchall()
        if result:
            df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
            logging.info("Fetched records successfully from aadhar table.")
            return df
        else:
            logging.info("No records found.")
            return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error fetching records: {e}")
        return pd.DataFrame()

def check_duplicacy(text_info):
    try:
        df = fetch_records(text_info)
        if df.shape[0] > 0:
            logging.info("Duplicate records found.")
            return True
        else:
            logging.info("No duplicate records found.")
            return False
    except Exception as e:
        logging.error(f"Error checking duplicacy: {e}")
        return False
    
def check_duplicacy_aadhar(text_info):
    try:
        df = fetch_records_aadhar(text_info)
        if df.shape[0] > 0:
            logging.info("Duplicate records found.")
            return True
        else:
            logging.info("No duplicate records found.")
            return False
    except Exception as e:
        logging.error(f"Error checking duplicacy: {e}")
        return False

