import os

class Config:
    
    # General Configurations
    SITE_NAME = "PGImporter" 
    DEBUG = True

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
    
