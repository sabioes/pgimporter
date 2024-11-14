import os

class Config:
    
    # General Configurations
    SITE_NAME = "PGImporter" 
    DEBUG = True
    ENV='development'

    # TODO
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    
    # Configuration of the paths for the core database importer module
    IMPORT_DUMP_PATH = os.getenv('IMPORT_DUMP_PATH', '/u02/pgbackup/db/postgres/import/')
    IMPORT_LOGS_PATH = os.getenv('IMPORT_LOGS_PATH', '/u02/pgbackup/db/postgres/import_logs/')
    EXPORT_DUMP_PATH = os.getenv('EXPORT_DUMP_PATH', '/u02/pgbackup/db/postgres/dumps/')

    # Database connection configuration
    DB_HOSTNAME = ""
    DB_PORT = ""
    DB_DATABASE = ""
    DB_USERNAME = ""
    DB_PASSWORD = os.getenv('PGPASSWORD', '')

    DATABASES = {
        'db1': {
            'hostname': 'db1.localhost',
            'port': 5432,
            'username': 'user1',
            'password': 'pass1'
        },
        'db2': {
            'hostname': 'db2.localhost',
            'port': 5432,
            'username': 'user2',
            'password': 'pass2'
        },
        'db3': {
            'hostname': 'db3.localhost',
            'port': 5432,
            'username': 'user3',
            'password': 'pass3'
        }
    }
    
