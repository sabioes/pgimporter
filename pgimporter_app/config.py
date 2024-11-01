import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    IMPORT_DUMP_PATH = os.getenv('IMPORT_DUMP_PATH', '/u02/pgbackup/db/postgres/import/')
    IMPORT_LOGS_PATH = os.getenv('IMPORT_LOGS_PATH', '/u02/pgbackup/db/postgres/import_logs/')
    EXPORT_DUMP_PATH = os.getenv('EXPORT_DUMP_PATH', '/u02/pgbackup/db/postgres/dumps/')
    DEBUG = True