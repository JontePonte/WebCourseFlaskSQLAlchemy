import flask

import pypi_org.services.package_service as package_service

blueprint = flask.Blueprint("packages", __name__, template_folder="templates")


@blueprint.route("/project/<package_name>")
def package_details(package_name: str):
    if not package_name:
        return flask.abort(status=404)

    package = package_service.get_package_by_id(package_name.strip().lower())
    if not package:
        return flask.abort(status=404)
    
    latest_release = None
    latest_version = "0.0.0"
    is_latest = True

    if package.releases:
        latest_release = package.releases[0]
        latest_version = latest_release.version_text
        is_latest = True

    return flask.render_template(
        "packages/details.html",
        package=package,
        latest_release=latest_release,
        latest_version=latest_version,
        is_latest=True,
        )


@blueprint.route("/<int:rank>")
def popular(rank: int):
    return "The details for the {}th popular package".format(rank)
