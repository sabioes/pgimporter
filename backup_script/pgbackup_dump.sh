#! /bin/bash

export PATH=$PATH:/u01/app/postgres/product/14.2/bin/

#Set here the variables and their values
DATE=$(date '+%Y-%m-%d_%H:%M:%S')

BD_USERNAME="postgres"
DB_NAME="postgres"
DB_DUMP_FILES_NAME="dev110-staging-system-2-dump"
DB_DUMP_OUTPUT_DIR_PATH="/u02/pgbackup/db/$DB_NAME/dumps"


execute_backup() {
	sudo su - postgres
	pg_dump -U ${BD_USERNAME} ${DB_NAME} > ${DB_DUMP_OUTPUT_DIR_PATH}/${DB_DUMP_FILES_NAME}_${DATE}.sql --verbose 2>${DB_DUMP_OUTPUT_DIR_PATH}/${DB_DUMP_FILES_NAME}_${DATE}.log
}

check_variables() {
	if  [ ! -n ${BD_NAME} ]; then
		echo "The var DB_NAME is empty!"
	fi
	if [ ! -d ${DB_DUMP_OUTPUT_DIR_PATH} ]; then
		  mkdir -p ${DB_DUMP_OUTPUT_DIR_PATH};
	fi
}

print_variables() {
	echo "Database Name: $DB_NAME"
}

echo "Staring the backup script"
check_variables

echo "Printing the script variables."
print_variables

echo "Backuping database $DB_NAME with following arguments"
execute_backup

echo "Backup finished sucessfully!"
