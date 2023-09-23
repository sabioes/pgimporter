
import os

from flask import render_template, send_file, request, Flask
from werkzeug.utils import secure_filename
from pgimporter_app.pgimporter import Pgimporter
from . import app

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/import/", methods=['GET','POST'])
def dashboardimport():
    items = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import/')
    if request.method == 'GET':
        return render_template("import.html", result='<div class="alert" role="alert"> Choose a dump to import.</div>', items=items)
    if request.method == 'POST':
        return render_template("import.html", result='<div class="alert" role="alert"> Choose a dump to import.</div>', items=items)

#items = ["Item 1", "Item 2", "Item 3"]

@app.route("/")
def dashboarddumps():
    
    items = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/dumps/')
    return render_template('dumps.html', items=items)

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

@app.route('/import/<filename>')
def import_dump(filename):
    #pass the filename to method import_dump() of pgimporter
    result = Pgimporter.import_dump(filename)
    return render_template("import.html", result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0')