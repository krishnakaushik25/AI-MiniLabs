import yaml
import os
import logging

def file_exists(file_path):
    is_exist = os.path.exists(file_path)
    if is_exist:
        logging.info(f"File exists at {file_path}")
        return True
    else:
        logging.warning(f"File does not exist at {file_path}")
        return False

# It will receive file path and if found return yes else no

def read_yaml(path_to_yaml:str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml  file: {path_to_yaml} loaded successfully")
    return content

# In this example, the config.yaml file is read and parsed into a dictionary, which is then printed out. The logging message "yaml file: config.yaml loaded successfully" would also be generated if logging is properly configured.

def create_dirs(dirs: list):
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        logging.info(f"Directory is created at {dir}")

# When you run this example, you will see log messages indicating that each directory has been created. If any of the directories already exist, they will be ignored, and no error will be raised due to the exist_ok=True parameter. I will be passing the list and exist_ok will ensure duplicy is not achieved 