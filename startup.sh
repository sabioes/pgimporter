#/bin/bash
#export PATH=/home/postgres/.local/bin:$PATH
#echo ${PATH}

#if [ ${EUID} -ne 54321 ];
#then 
    # this means to be runned as postgres user
#    exit 1 
#fi

#cd /u02/pgbackup/pgimporter
 
#gunicorn --bind=0.0.0.0 --workers=4 startup:app --daemon
gunicorn --bind=0.0.0.0 --workers=4 startup:app 
