__author__ = 'IBM'

from flask import Flask
from flask import send_from_directory, render_template, request
from qpylib import qpylib

app = Flask(__name__)
# Create log here to prevent race condition when importing views
qpylib.create_log()

from app import views

@app.route('/debug')
def debug():
    return send_from_directory( '/store/log/', 'app.log' )

@app.route('/debug_view')
def debug_view():
    debug_content = open('/store/log/app.log').read()
    return render_template('debug.html', debug_content=debug_content)

@app.route('/resources/<path:file>')
def send_file(file):
    qpylib.log(" >>> route resources >>>")
    qpylib.log(" file=" + file)
    qpylib.log(" app.static_folder=" + app.static_folder)
    qpylib.log(" full file path =" + app.static_folder + '/resources/'+file )
    return send_from_directory(app.static_folder, 'resources/'+file)

@app.route('/log_level', methods=['POST'])
def log_level():
    level = request.form['level'].upper()
    levels = ['INFO', 'DEBUG', 'ERROR', 'WARNING', 'CRITICAL']

    if any( level in s for s in levels):
        qpylib.set_log_level(request.form['level']) 
    else:
        return 'level parameter missing or unsupported - ' + str (levels), 42
    return 'log level set to ' + level

#register the new q_url_for() method for use with Jinja2 templates
app.jinja_env.globals.update(q_url_for=q_url_for)
