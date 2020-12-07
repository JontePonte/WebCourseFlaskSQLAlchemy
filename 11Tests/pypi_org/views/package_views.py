import flask

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.viewmodels.package.packagedetails_viewmodel import PackageDetailsViewModel

blueprint = flask.Blueprint("packages", __name__, template_folder="templates")


@blueprint.route("/project/<package_name>")
@response(template_file="packages/details.html")
def package_details(package_name: str):
    vm = PackageDetailsViewModel(package_name)

    if not vm.package_name:
        return flask.abort(status=404)

    return vm.to_dict()


@blueprint.route("/<int:rank>")
def popular(rank: int):
    return "The details for the {}th popular package".format(rank)
