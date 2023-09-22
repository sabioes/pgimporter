from flask import Flask
from flask import render_template, send_file, request
from werkzeug.utils import secure_filename
import os

from pgimporter_app.pgimporter import Pgimporter
from . import app

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/import/")
def dashboardimport():
    return render_template("import.html")

#items = ["Item 1", "Item 2", "Item 3"]

@app.route("/")
def dashboarddumps():
    
    items = Pgimporter.read_dumps()
    return render_template("dumps.html", items=items)

@app.route('/download/<filename>')
def download_file(filename):
    
    # Define the path to the file you want to serve
    file_path = f'/u02/pgbackup/db/postgres/dumps/{filename}'  # Replace with the actual path to your files

    # Use send_file to send the file to the user's browser
    return send_file(file_path, as_attachment=True)

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template("import.html", result='<div class="alert alert-warning" role="alert">No file provided!</div>')
    
    file = request.files['file']
    
    if file.filename == '': return render_template("import.html", result='<div class="alert alert-warning" role="alert">No file selected.</div>')
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('/u02/pgbackup/db/postgres/import', filename))
        result='<div class="alert alert-success" role="alert">File uploaded successfully.</div>'
        return render_template("import.html", result=result)

