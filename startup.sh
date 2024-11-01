#/bin/bash
#export PATH=/home/postgres/.local/bin:$PATH
#echo ${PATH}

#if [ ${EUID} -ne 54321 ];
#then 
    # this means to be runned as postgres user
#    exit 1 
#fi

#cd /u02/pgbackup/pgimporter
 
gunicorn --bind=0.0.0.0 --timeout 60 --threads 3 --workers 4 "pgimporter_app:create_app()"
