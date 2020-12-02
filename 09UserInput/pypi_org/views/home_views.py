import flask

import pypi_org.services.package_service as package_service
import pypi_org.services.user_service as user_service
import pypi_org.infrastructure.cookie_auth as cookie_auth

blueprint = flask.Blueprint("home", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    return flask.render_template(
        "home/index.html",
        releases=package_service.get_latest_releases(),
        package_count=package_service.get_package_count(),
        release_count=package_service.get_release_count(),
        user_count=user_service.get_user_count(),
        user_id=cookie_auth.get_user_id_via_auth_cookie(flask.request),
    )


@blueprint.route("/about")
def about():
    return flask.render_template("home/about.html")
