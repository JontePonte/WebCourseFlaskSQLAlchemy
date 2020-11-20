import flask

import pypi_org.services.package_service as package_service

blueprint = flask.Blueprint('packages', __name__, template_folder='templates')


@blueprint.route('/project/<package_name>')
def package_details(package_name: str):
    # return "Package details for {}".format(package_name)
    return flask.render_template('packages/details.html', package_name=package_name)


@blueprint.route('/<int:rank>')
def popular(rank:int):
    return "The details for the {}th popular package".format(rank)
