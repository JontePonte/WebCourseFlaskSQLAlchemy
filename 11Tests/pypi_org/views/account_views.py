import flask

import pypi_org.services.user_service as user_service
import pypi_org.infrastructure.cookie_auth as cookie_auth
import pypi_org.infrastructure.request_dict as request_dict

from pypi_org.viewmodels.account.index_viewmodel import IndexViewModel
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel
from pypi_org.viewmodels.account.login_viewmodel import LoginViewModel
from pypi_org.infrastructure.view_modifiers import response

blueprint = flask.Blueprint("account", __name__, template_folder="templates")


""" --------------- Account --------------- """


@blueprint.route("/account")
@response(template_file="account/index.html")
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')

    return vm.to_dict()


""" --------------- Register --------------- """


@blueprint.route("/account/register", methods=["GET"])
@response(template_file="account/register.html")
def register_get():
    return {'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request)}


@blueprint.route("/account/register", methods=["POST"])
@response(template_file="account/register.html")
def register_post():
    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The accout could not be created'
        return vm.to_dict()

    resp = flask.redirect("/account")
    cookie_auth.set_auth(resp, user.id)

    return resp


""" --------------- Login --------------- """


@blueprint.route("/account/login", methods=["GET"])
@response(template_file="account/login.html")
def login_get():
    vm = LoginViewModel()
    return vm.to_dict()


@blueprint.route("/account/login", methods=["POST"])
@response(template_file="account/login.html")
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = "The account does not exist or the password is wrong"
        return vm.to_dict()

    resp = flask.redirect("/account")
    cookie_auth.set_auth(resp, user.id)

    return resp


""" --------------- Logout --------------- """


@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp
