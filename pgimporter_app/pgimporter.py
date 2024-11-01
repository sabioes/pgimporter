import os, datetime, subprocess

from flask import flash

class Pgimporter:
    @staticmethod
    def read_dumps(folder_path):
        
        # Initialize an empty list to store file information
        file_info_list = []

        try:
            # Iterate over the files in the specified folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                # Check if the item is a file (not a directory)
                if os.path.isfile(file_path):

                    file_type_bs_color = " "
                    file_extension = " "
                    try:
                        filename.split(".")[1]
                    except:
                        file_type_bs_color = "secondary"
                        file_extension = "Other"
                    else:
                        file_type_bs_color = "info" if filename.split(".")[1] == "sql" else "primary"
                        file_extension = filename.split(".")[1]

                    file_type = '<span class="badge bg-'+ file_type_bs_color +'">'+ file_extension +'</span>'

                    # Get the size of the file in bytes
                    file_size = os.path.getsize(file_path)

                    # Extract the creation timestamp (ctime) from the file_stat
                    creation_timestamp = os.stat(file_path).st_ctime

                    # Convert the timestamp to a human-readable date format
                    file_creation_date = datetime.datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

                    # Append the filename and its size to the list
                    file_info_list.append((file_type, filename, file_size, file_creation_date))
            return file_info_list
        except FileNotFoundError as ex:
            flash("No dir or file discovered", "danger")
            print("No dir or file discovered")
            return file_info_list
        # Now, file_info_list contains tuples of (filename, file_size)
        # You can use this list to access the file names and their sizes
        #for filename, file_size in file_info_list:
        #    print(f"File: {filename}, Size: {file_size} bytes")
        
    
    @staticmethod
    def import_dump(dump_filename):
        #https://stackoverflow.com/questions/43380273/pg-dump-pg-restore-password-using-python-module-subprocess
        #Run the OS level command "pg_dump postgres"
        #if dump_filename.split(".")[1] != "sql": return "Incorrect dump file: " + dump_filename.split(".")[1]


        # Replace 'command' with the actual command you want to run
        absdumppath = '/u02/pgbackup/db/postgres/import/' + dump_filename
        
        database = 'postgres'
        #pg_restore --verbose -d dbname filename
        #psql -U postgres -d postgres < <DB_DUMPFILE> -a 1>import-database-out<LOG_FILE_SUFFIX>.log 2>import-database-error<LOG_FILE_SUFFIX>.log
        #pg_dump postgres --verbose > ats110-after-qf.sql | tee pg_dump_ats110_after_qf_execution.log
        
        command = 'pg_dump ' + database + ' --verbose > ' + absdumppath         
        uid = 54321
        
        try:
            print("Running the pg_dump command: " + command)
            result = subprocess.run(command, check=True, shell=True, preexec_fn=lambda: os.setuid(uid), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            #result = result.stderr
            #formatted_result = result.replace('\\n', '\n').replace('\\t', '\t')
            
            result_file = open('/u02/pgbackup/db/postgres/import_logs/pg_dump_result_'+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.log', 'w')
            result_file.write(result.stderr.decode())
            result_file.close()
            
            if result.returncode == 0 : return "Import Succeeded!" 
            else: return "Import not Succeeded!"
        except subprocess.CalledProcessError as e:
            # Handle errors
            return(f"Command failed with error: {e.returncode}\n{e.output}")
