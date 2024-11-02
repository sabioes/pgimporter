import os
import datetime
import subprocess
from flask import flash

class Pgimporter:
    
    @staticmethod
    def read_dumps(folder_path):
        """Reads dump files in the specified folder and returns a list of file information."""
        file_info_list = []

        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(filename)[1][1:] or "Other"
                    file_type_bs_color = "info" if file_extension == "sql" else "primary" if file_extension else "secondary"
                    file_type = f'<span class="badge bg-{file_type_bs_color}">{file_extension}</span>'

                    file_size = os.path.getsize(file_path)
                    file_creation_date = datetime.datetime.fromtimestamp(
                        os.path.getctime(file_path)
                    ).strftime('%Y-%m-%d %H:%M:%S')

                    file_info_list.append((file_type, filename, file_size, file_creation_date))

            return file_info_list

        except FileNotFoundError:
            flash("No directory or file discovered", "danger")
            print("No directory or file discovered")
            return file_info_list

    @staticmethod
    def import_dump(dump_filename):
        """Executes a pg_dump command for the specified dump file."""
        abs_dump_path = os.path.join('/u02/pgbackup/db/postgres/import', dump_filename)
        import_log_path = os.path.join(
            '/u02/pgbackup/db/postgres/import_logs',
            f'pg_dump_result_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
        )

        command = f'pg_dump postgres --verbose > {abs_dump_path}'
        uid = 54321

        try:
            print(f"Running the pg_dump command: {command}")
            result = subprocess.run(
                command,
                check=True,
                shell=True,
                preexec_fn=lambda: os.setuid(uid),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Write stderr output to log file
            with open(import_log_path, 'w') as result_file:
                result_file.write(result.stderr.decode())

            return "Import Succeeded!" if result.returncode == 0 else "Import Not Succeeded!"

        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with error code {e.returncode}: {e.stderr.decode()}"
            print(error_message)
            return error_message
