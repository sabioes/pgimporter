
# PGImporter

This tool is intended to be used as support tool speed up the download of database dumps and import dumps in database. The is to be executed parallelly with database server in same virtual machine

## Installation of PGimporter

### Linux

#### Ubuntu

Update and upgrade the package from apt repositories:

```bash
  sudo apt update && sudo apt upgrade -y
```
Install the required dependency package:

```bash
  sudo apt install software-properties-common -y
```
   Add the deadsnakes PPA to the apt repository source list:

```bash
  sudo add-apt-repository ppa:deadsnakes/ppa
```
Install Python 3.11:

```bash
  sudo apt install python3.11
```
Install pip for Python 3.11:

```bash
  curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 
```
## Setup Backup Routine

### Linux

Go to backup script directory:

```bash
  cd backup_script/
```

Check the bash variables in script file:

```bash
  pgbackup_dump.sh
```
Create a cron table entry to schedule the backup hourly/daily/weekly:

```bash
  crontab -e
  
  30 0 * * * postgres /u02/pgbackup/pgbackup_dump.sh
```
*(example). Obs.: Expression editor, here look: Crontab.guru - The cron schedule expression editor*

## Run PGImporter 

### Starting PGImporter

Clone the project:

```bash
  git clone https://link-to-project
```

Go to the project directory:

```bash
  cd pgimporter
```

Install dependencies:

```bash
  pip3.11 install -r requirements.txt
```

Start the Gunicorn server with 4 threads as daemon:

```bash
  gunicorn --bind=0.0.0.0 --workers=4 startup:app --daemon
```

### Stop PGImporter

Check all Gunicorn process:

```bash
  lsof -i:8000
```

Kill all Gunicorn process:

```bash
  pkill gunicorn
```

## Running Tests

To run tests, run the following commands


Execute the pytests:

```bash
  python3.11 -m test
```
## Authors

- [@carlossilva](https://www.linkedin.com/in/carlosilvas/)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## How to contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.

