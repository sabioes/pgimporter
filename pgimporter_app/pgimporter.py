import os

class Pgimporter:
    @staticmethod
    def read_imports():

        # Specify the path to the folder you want to analyze
        folder_path = 'C:\Workspace\Learn Projects\pgimporter\pgimporter_app'

        # Initialize an empty list to store file information
        file_info_list = []

        # Iterate over the files in the specified folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if the item is a file (not a directory)
            if os.path.isfile(file_path):
                # Get the size of the file in bytes
                file_size = os.path.getsize(file_path)

                # Append the filename and its size to the list
                file_info_list.append((filename, file_size))

        # Now, file_info_list contains tuples of (filename, file_size)
        # You can use this list to access the file names and their sizes
        #for filename, file_size in file_info_list:
        #    print(f"File: {filename}, Size: {file_size} bytes")
        return file_info_list
