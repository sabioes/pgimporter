import json
import os

class Config:
    
    # General Configurations
    __FILE_NAME = "data.json"
    SITE_NAME = "PGImporter" 
    DEBUG = True
    ENV='development'
    

    # TODO
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    
    # Configuration of the paths for the core database importer module
    IMPORT_DUMP_PATH = os.getenv('IMPORT_DUMP_PATH', '/u02/pgbackup/db/postgres/import/')
    IMPORT_LOGS_PATH = os.getenv('IMPORT_LOGS_PATH', '/u02/pgbackup/db/postgres/import_logs/')
    EXPORT_DUMP_PATH = os.getenv('EXPORT_DUMP_PATH', '/u02/pgbackup/db/postgres/dumps/')

    # Databases connection properties
    DATABASES = {
        'db1': {
            'hostname': 'localhost',
            'port': 5432,
            'username': 'user1',
            'password': 'pass1'
        },
        'db2': {
            'hostname': 'localhost',
            'port': 5432,
            'username': 'user2',
            'password': 'pass2'
        },
        'db3': {
            'hostname': 'localhost',
            'port': 5432,
            'username': 'user3',
            'password': 'pass3'
        }
    }
    # method to load data configuration from file
    @staticmethod
    def loadConfigs():    
        #Custom function to load database connection properties.
        with open(Config.__FILE_NAME, 'r') as file:
            Config.DATABASES = json.load(file)
        
    # method to save data configuration to file
    @staticmethod
    def saveConfigs(data):        
    # Open the file in write mode and save the dictionary as JSON
        with open(Config.__FILE_NAME, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # indent=4 adds indentation for readability
    
