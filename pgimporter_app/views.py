import os
import lesscpy # type: ignore
from flask import  Blueprint, abort, current_app, flash, render_template, request, redirect, send_file, url_for # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from pgimporter_app.pgimporter import Pgimporter
from .pgimporter import Pgimporter
from .config import Config

main_blueprint = Blueprint('main', __name__)

def compile_less():
    less_file_path = 'pgimporter_app/static/less/jumbotron.less'
    css_file_path = 'pgimporter_app/static/css/styles.css'

    #print("Compling less!!!")

    # Check if the LESS file exists
    if not os.path.isfile(less_file_path):
        flash("The LESS file not exists", "danger")
        #print("NO FILE FOUND!")
        return

    try:
        # Read the LESS file
        with open(less_file_path, 'r') as less_file:
            less_content = less_file.read()

        # Compile LESS to CSS
        #css_content = lesscpy.compile(less_content)

        # Write the compiled CSS to the output file
        #with open(css_file_path, 'a') as css_file:
            # css_file.write(css_content)
            #css_file.write(less_content)
        flash("Successfully compiled '{less_file_path}' to '{css_file_path}'.","success")
        print("FUNCIONA!")

    except Exception as e:
        flash("An error occurred: {e}","danger")
        print(f"DEU MERDA!:", e)

@main_blueprint.before_request
def before_request():
    compile_less()  # Compile LESS before every request

@main_blueprint.route("/")
def dashboarddumps():
    try:
        dumps_path = current_app.config['EXPORT_DUMP_PATH']
        items = Pgimporter.read_dumps(dumps_path)
    except Exception as e:    
        flash("Error loading dumps.", "danger")
        current_app.logger.error(f"Failed to load dumps: {e}")
        items = []
    return render_template('dumps.html', items=items)

@main_blueprint.route("/about")
def about():
    # Render the About page with error handling.
    try: 
        return render_template("about.html")
    except Exception as e:
        flash("An error occurred while trying to load the About page. Please try again later.", "error")
        return redirect(url_for('main_blueprint.index'))  # Redirect to a safe page, like the homepage

@main_blueprint.route("/config", methods=['GET','POST'])
def config():
    if request.method == 'GET':
        # Render the Configurations page with error handling.
        try:
            return render_template("config.html", configs=current_app.config)
        except Exception as e:
            flash("An error occurred while trying to load the Configuration page. Please try again later.", "error")
            return redirect(url_for('main.config'))
    if request.method == 'POST':
        try:
            current_app.config['SITE_NAME'] = request.form.get('site_name')
            current_app.config['IMPORT_DUMP_PATH'] = request.form.get('import_dump_path')
            current_app.config['IMPORT_LOGS_PATH'] = request.form.get('import_logs_path')
            current_app.config['EXPORT_DUMP_PATH'] = request.form.get('export_dump_path')
            
            Config.saveConfigs(request.get_json())
            return render_template("config.html", configs=current_app.config)
        except Exception as e:
            flash("An error occurred while trying to post the Configuration. Please try again later.", "error")
            return redirect(url_for('main.config'))

@main_blueprint.route("/import", methods=['GET','POST'])
def dashboardimport():
    def render_import_page(result_message):
        """Helper function to render the import page with SQL files and logs."""
        import_sql_files = Pgimporter.read_dumps(current_app.config['IMPORT_DUMP_PATH'])
        import_logs = Pgimporter.read_dumps(current_app.config['IMPORT_LOGS_PATH'])
        return render_template("import.html", result=result_message, import_sql_files=import_sql_files, import_logs=import_logs)
    
    if request.method == 'GET':
        # GET request to load the dumps files and logs in dashboard
        # return render_template("import.html", result='<div class="alert alert-secondary" role="alert"> Choose a dump to import.</div>', import_sql_files=import_sql_files, import_logs=import_logs)
        return render_import_page('<div class="alert alert-secondary" role="alert">Choose a dump to import.</div>')

    if request.method == 'POST':
        # POST request to handle the dump file upload
        file = request.files['file']
        if not file or file.filename == '': 
            return render_import_page('<div class="alert alert-warning" role="alert">No file selected.</div>')
        else:
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(Config.IMPORT_DUMP_PATH, filename)
                file.save(file_path)
                result_message='<div class="alert alert-success" role="alert">File uploaded successfully.</div>'
            except OSError as e:
                current_app.logger.error(f"File upload failed: {e}")
                flash("File upload failed: {e}", "danger")
                result_message = f'<div class="alert alert-danger" role="alert">Unexpected error on upload: {e.strerror}</div>'
        #return render_template("import.html", result=result, import_sql_files=import_sql_files, import_logs=import_logs)
        return render_import_page(result_message)

@main_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Define file paths based on the request argument 'type'
    file_type = request.args.get('type')
    file_paths = {
        'dump': current_app.config['DUMPS_PATH'],
        'import': current_app.config['IMPORT_PATH'],
        'import_logs': current_app.config['IMPORT_LOGS_PATH']
    }
    
    # Validate the file type
    base_path = file_paths.get(file_type)
    if not base_path:
        flash("Invalid file type specified.", "danger")
        abort(400, description="Invalid file type specified.")
    
    # Construct the full file path and check if the file exists
    file_path = os.path.join(base_path, filename)
    if not os.path.isfile(file_path):
        flash("File not found.", "warning")
        abort(404, description="File not found.")
    
    # Serve the file for download
    return send_file(file_path, as_attachment=True)


@main_blueprint.route('/import/<filename>')
def import_dump(filename):
    try:
        # Pass the filename to the import_dump() method of Pgimporter
        Pgimporter.import_dump(filename)
        flash("File imported successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Failed to import file {filename}: {e}")
        flash("Error importing file. Please try again.", "danger")
    
    # Redirect to the import page
    return redirect(url_for('main_blueprint.dashboardimport'))

#TODO
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