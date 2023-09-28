
import os

from flask import render_template, send_file, request, Flask
from werkzeug.utils import secure_filename
from pgimporter_app.pgimporter import Pgimporter
from . import app

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/import", methods=['GET','POST'])
def dashboardimport():
    
    if request.method == 'GET':
        import_sql_files = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import/')
        import_logs = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import_logs/')
        return render_template("import.html", result='<div class="alert alert-secondary" role="alert"> Choose a dump to import.</div>', import_sql_files=import_sql_files, import_logs=import_logs)
    if request.method == 'POST':
        #if 'file' not in request.files:
        #   result='<div class="alert alert-warning" role="alert">No file provided!</div>'
    
        file = request.files['file']
    
        if file.filename == '': 
            result='<div class="alert alert-warning" role="alert">No file selected.</div>'
        elif file:
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join('/u02/pgbackup/db/postgres/import', filename))
                result='<div class="alert alert-success" role="alert">File uploaded successfully.</div>'
            except OSError as e:
                result='<div class="alert alert-danger" role="alert">Unexpected Error on upload:'+ e.strerror +'</div>' 
        
        import_sql_files = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import/')
        import_logs = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import_logs/')

        return render_template("import.html", result=result, import_sql_files=import_sql_files, import_logs=import_logs)

#items = ["Item 1", "Item 2", "Item 3"]

@app.route("/")
def dashboarddumps():
    
    items = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/dumps/')
    return render_template('dumps.html', items=items)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    
    # Define the path to the file you want to serve
    if request.args.get('type') == 'dump':
        file_path = f'/u02/pgbackup/db/postgres/dumps/{filename}'
    elif request.args.get('type') == 'import':
        file_path = f'/u02/pgbackup/db/postgres/import/{filename}'
    elif request.args.get('type') == 'import_logs':
        file_path = f'/u02/pgbackup/db/postgres/import_logs/{filename}'
    
    # Use send_file to send the file to the user's browser
    return send_file(file_path, as_attachment=True)


#TO DELETE AFTER TESTING
#@app.route('/upload', methods=['GET','POST'])
#def upload_file():
#    if 'file' not in request.files:
#        return render_template("import.html", result='<div class="alert alert-warning" role="alert">No file provided!</div>')
#    
#    file = request.files['file']
#    
#    if file.filename == '': return render_template("import.html", result='<div class="alert alert-warning" role="alert">No file selected.</div>')
#    
#    if file:
#        filename = secure_filename(file.filename)
#        file.save(os.path.join('/u02/pgbackup/db/postgres/import', filename))
#        result='<div class="alert alert-success" role="alert">File uploaded successfully.</div>'
#        return render_template("import.html", result=result)

@app.route('/import/<filename>')
def import_dump(filename):
    #pass the filename to method import_dump() of pgimporter
    result = Pgimporter.import_dump(filename)
    import_sql_files = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import/')
    import_logs = Pgimporter.read_dumps('/u02/pgbackup/db/postgres/import_logs/')
    return render_template("import.html", result=None, import_sql_files=import_sql_files, import_logs=import_logs)

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')