import flask

import pypi_org.services.user_service as user_service
import pypi_org.infrastructure.cookie_auth as cookie_auth
import pypi_org.infrastructure.request_dict as request_dict

from pypi_org.viewmodels.account.index_viewmodel import IndexViewModel

blueprint = flask.Blueprint("account", __name__, template_folder="templates")


""" --------------- Account --------------- """


@blueprint.route("/account")
def index():
    vm = IndexViewModel() 
    if not vm.user_id:
        return flask.redirect('/account/login')

    return flask.render_template(
        "account/index.html",
        vm.to_dict()
        )


""" --------------- Register --------------- """


@blueprint.route("/account/register", methods=["GET"])
def register_get():
    return flask.render_template("account/register.html")


@blueprint.route("/account/register", methods=["POST"])
def register_post():

    data = request_dict.create()

    name = data.name
    email = data.email.lower().strip()
    password = data.password.strip()

    if not name or not email or not password:
        return flask.render_template(
            "account/register.html",
            name=name,
            email=email,
            password=password,
            error="Some required fields are missing.",
        )

    user = user_service.create_user(name, email, password)
    if not user:
        return flask.render_template(
            "account/register.html",
            name=name,
            email=email,
            password=password,
            error="A user with that email already exists.",
        )
    resp = flask.redirect("/account")
    cookie_auth.set_auth(resp, user.id)

    return resp


""" --------------- Login --------------- """


@blueprint.route("/account/login", methods=["GET"])
def login_get():
    return flask.render_template("account/login.html")


@blueprint.route("/account/login", methods=["POST"])
def login_post():
    data = request_dict.create()

    email = data.email.lower().strip()
    password = data.password.strip()

    if not email or not password:
        return flask.render_template(
            "account/login.html",
            email=email,
            password=password,
            error="Please enter email and password.",
        )

    user = user_service.login_user(email, password)
    if not user:
        return flask.render_template(
            "account/login.html",
            email=email,
            password=password,
            error="The account does not exist or the password is wrong.",
        )

    resp = flask.redirect("/account")
    cookie_auth.set_auth(resp, user.id)

    return resp


""" --------------- Logout --------------- """


@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp
