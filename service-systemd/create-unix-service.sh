#/bin/bash

SERVICE_DIR="/home/postgres/.config/systemd/user"

if [ ! -d ${SERVICE_DIR} ]; then
    mkdir -p ${SERVICE_DIR};
fi

chmod +x /u02/pgbackup/pgimporter/startup.sh

cp PGIMPORTER.service ${SERVICE_DIR}/PGIMPORTER.service

systemctl --user daemon-reload

systemctl --user enable PGIMPORTER.service

systemctl --user is-enabled PGIMPORTER.service