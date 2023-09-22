import os, datetime
from flask import send_file

class Pgimporter:
    @staticmethod
    def read_dumps():

        # Specify the path to the folder you want to analyze
        folder_path = '/u02/pgbackup/db/postgres/dumps/'

        # Initialize an empty list to store file information
        file_info_list = []

        # Iterate over the files in the specified folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if the item is a file (not a directory)
            if os.path.isfile(file_path):
                
                file_type_bs_color = "info" if filename.split(".")[1] == "sql" else "primary"
                file_type = '<span class="badge badge-pill badge-'+ file_type_bs_color +'">'+filename.split(".")[1]+'</span>'
                
                # Get the size of the file in bytes
                file_size = os.path.getsize(file_path)
                
                # Extract the creation timestamp (ctime) from the file_stat
                creation_timestamp = os.stat(file_path).st_ctime

                # Convert the timestamp to a human-readable date format
                file_creation_date = datetime.datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

                # Append the filename and its size to the list
                file_info_list.append((file_type, filename, file_size, file_creation_date))

        # Now, file_info_list contains tuples of (filename, file_size)
        # You can use this list to access the file names and their sizes
        #for filename, file_size in file_info_list:
        #    print(f"File: {filename}, Size: {file_size} bytes")
        return file_info_list