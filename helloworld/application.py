#!flask/bin/python
import optparse
from flask import Flask, flash, redirect, render_template, send_file, session, url_for
from flask_executor import Executor
from helloworld.forms import GenerateSiteMapForm, PathForm, UploadForm
from helloworld.services import analyze_page, create_analyst, download_db, upload_nodes
import os
from urllib.parse import urlparse
from werkzeug.utils import secure_filename


application = Flask(__name__)
executor = Executor(application)
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default='A very terrible secret key.')
basedir = os.path.abspath(os.path.dirname(__file__))


@application.before_request
def before_request():
    if 'parameters' not in session:
        session['parameters'] = dict()
    if 'analysis_running' not in session:
        session['analysis_running'] = False
    if 'short_path' not in session:
        session['short_path'] = []


@application.route('/', methods=['GET', 'POST'])
def index():
    map_form = GenerateSiteMapForm(prefix='map')
    path_form = PathForm(prefix='path')
    upload_form = UploadForm()
    if executor.futures.done('analyze'):
        session['analysis_running'] = False
        future = executor.futures.pop('analyze')
        session['parameters'] = future.result()
    return render_template('index.html',
                           map_form=map_form,
                           path_form=path_form,
                           upload_form=upload_form,
                           page_parameters=session['parameters'],
                           short_path=session['short_path'],
                           in_progress=session['analysis_running'])


@application.route('/map', methods=['POST'])
def map_page():
    map_form = GenerateSiteMapForm(prefix='map')
    if map_form.validate_on_submit():
        executor.submit_stored('analyze', analyze, url=map_form.start_page.data)
        session['analysis_running'] = True
        session['parameters'] = dict()
        session['short_path'] = []
        flash('Analysis started, page will reload automatically. This can take a time.')
    else:
        flash_errors(map_form)
    return redirect(url_for('index'))


@application.route('/path', methods=['POST'])
def short_path():
    path_form = PathForm(prefix='path')
    if path_form.validate_on_submit():
        session['short_path'] = get_shortest_path(path_form.source.data, path_form.target.data)
    else:
        flash_errors(path_form)
    return redirect(url_for('index'))


@application.route('/download_db')
def download_file():
    return send_file(download_db(), as_attachment=True)


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        filename = secure_filename(upload_form.file.data.filename)
        if '.' in filename and filename.rsplit('.', 1)[1].lower() == 'json':
            filepath = os.path.join(basedir, 'uploads', filename)
            upload_form.file.data.save(filepath)
            upload_nodes(filepath)
            executor.submit_stored('analyze', analyze, url=upload_form.start_page.data, local=True)
        else:
            flash("Wrong file extension, upload rejected.")
    return redirect(url_for('index'))


def get_shortest_path(source, target):
    analyst = create_analyst()
    return analyst.get_shortest_path(source, target)


def analyze(url="", local=False):
    parameters = dict()
    domain = urlparse(url).netloc
    if local:
        analyst = create_analyst()
    else:
        analyst = analyze_page(url)
    parameters['int_links_mean'] = analyst.average_number_of_internal_links(domain)
    parameters['ext_links_mean'] = analyst.average_number_of_external(domain)
    parameters['most_distant'] = analyst.most_distant_subpages(source=url)
    parameters['dead_links'] = analyst.get_dead_links(domain)
    parameters['most_difficult'] = analyst.most_difficult_to_enter_pages()
    parameters['most_linked'] = analyst.most_linked_pages()
    return parameters


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text} field - {error}")


if __name__ == '__main__':
    default_port = "80"
    default_host = "0.0.0.0"
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help=f"Hostname of Flask app {default_host}.",
                      default=default_host)

    parser.add_option("-P", "--port",
                      help=f"Port for Flask app {default_port}.",
                      default=default_port)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    application.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
