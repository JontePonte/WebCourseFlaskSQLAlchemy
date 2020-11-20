import flask

import pypi_org.services.package_service as package_service

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    test_packages = package_service.get_latest_packages()
    return flask.render_template('home/index.html', packages=test_packages)


@blueprint.route('/about')
def about():
    return flask.render_template('home/about.html')
