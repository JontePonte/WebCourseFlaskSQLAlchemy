import os
import sys

import unittest.mock
import flask

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel
from pypi_org.viewmodels.account.login_viewmodel import LoginViewModel
from pypi_org.data.users import User
from test_client import flask_app
from test_client import client


def test_example():
    print("Test example...")
    assert 1 + 2 == 3


""" -------------------- Account ----------------------- """


def test_view_account_not_logged_in():
    # Arrange
    from pypi_org.views.account_views import index
    user = None

    target = "pypi_org.services.user_service.find_user_by_id"
    find_user = unittest.mock.patch(target, return_value=user)
    request = flask_app.test_request_context(path="account")

    with find_user, request:
        # Act
        resp: flask.Response = index()

    # Assert
    assert resp.location == "/account/login"


def test_view_account_is_logged_in():
    # Arrange
    from pypi_org.views.account_views import index
    user = User()

    target = "pypi_org.services.user_service.find_user_by_id"
    find_user = unittest.mock.patch(target, return_value=user)
    target = "pypi_org.infrastructure.cookie_auth.get_user_id_via_auth_cookie"
    get_user_id = unittest.mock.patch(target, return_value=3)
    request = flask_app.test_request_context(path="account")

    with find_user, get_user_id, request:
        # Act
        resp: flask.Response = index()

    # Assert
    assert resp.location is None
    assert isinstance(resp.model.get('user'), User)


def test_int_account_home_no_login(client):
    target = 'pypi_org.services.user_service.find_user_by_id'
    with unittest.mock.patch(target, return_value=None):
        resp: flask.Response = client.get('/account')

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/account/login'


def test_int_account_home_with_login(client):
    target = 'pypi_org.services.user_service.find_user_by_id'
    test_user_p = User(name='ppppp', email='ppp@p.p')

    with unittest.mock.patch(target, return_value=test_user_p):
        resp: flask.Response = client.get('/account')

    assert resp.status_code == 200
    assert b'ppppp' in resp.data


""" -------------------- Login ----------------------- """


def test_login_validation_when_valid():
    # Arrange
    form_data = {"email": "john_nordstrand@hotmail.com", "password": "aaaaa"}

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = LoginViewModel()

    # Act
    vm.validate()

    # Assert
    assert vm.error is None


def test_login_validation_when_no_email():
    # Arrange
    form_data = {"email": " ", "password": "aaaaa"}

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = LoginViewModel()

    # Act
    vm.validate()

    # Assert
    assert vm.error is not None
    assert "specify a email" in vm.error


def test_login_validation_when_no_password():
    # Arrange
    form_data = {"email": "john_nordstrand@hotmail.com", "password": ""}

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = LoginViewModel()

    # Act
    vm.validate()

    # Assert
    assert vm.error is not None
    assert "specify a password" in vm.error


def test_view_login_user():
    # Arrange
    from pypi_org.views.account_views import login_post

    form_data = {
        "email": "john_nordstrand@hotmail.com",
        "password": "aaaaa",
    }

    target = "pypi_org.services.user_service.login_user"
    login_user = unittest.mock.patch(target, return_value=User())
    request = flask_app.test_request_context(path="account/register", data=form_data)

    with login_user, request:
        # Act
        resp: flask.Response = login_post()

    # Assert
    assert resp.location == "/account"


""" -------------------- Register ----------------------- """


def test_register_validation_when_valid():
    # Arrange
    form_data = {
        "name": "John",
        "email": "john_nordstrand@hotail.com",
        "password": "aaaaa",
    }

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = RegisterViewModel()

    # Act
    target = "pypi_org.services.user_service.find_user_by_email"
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is None


def test_register_validation_when_email_exist():
    # Arrange
    form_data = {
        "name": "John",
        "email": "john_nordstrand@hotail.com",
        "password": "aaaaa",
    }

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = RegisterViewModel()

    # Act
    target = "pypi_org.services.user_service.find_user_by_email"
    user = User()
    user.name = "John"
    user.email = "john_nordstrand@hotmail.com"
    with unittest.mock.patch(target, return_value=user):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert "email already exists" in vm.error


def test_register_validation_when_no_email():
    # Arrange
    form_data = {"name": "John", "email": "", "password": "aaaaa"}

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = RegisterViewModel()

    # Act
    target = "pypi_org.services.user_service.find_user_by_email"
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert "specify a email" in vm.error


def test_register_validation_when_no_password():
    # Arrange
    form_data = {
        "name": "John",
        "email": "john_nordstrand@hotmail.com",
        "password": " ",
    }

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = RegisterViewModel()

    # Act
    target = "pypi_org.services.user_service.find_user_by_email"
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert "specify a password" in vm.error


def test_register_validation_when_short_password():
    # Arrange
    form_data = {
        "name": "John",
        "email": "john_nordstrand@hotmail.com",
        "password": "aaaa",
    }

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = RegisterViewModel()

    # Act
    target = "pypi_org.services.user_service.find_user_by_email"
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert "Password needs" in vm.error


def test_register_validation_when_no_name():
    # Arrange
    form_data = {
        "name": " ",
        "email": "john_nordstrand@hotmail.com",
        "password": "aaaaa",
    }

    with flask_app.test_request_context(path="account/register", data=form_data):
        vm = RegisterViewModel()

    # Act
    target = "pypi_org.services.user_service.find_user_by_email"
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert "specify a name" in vm.error


def test_view_register_new_user():
    # Arrange
    from pypi_org.views.account_views import register_post

    form_data = {
        "name": "John",
        "email": "john_nordstrand@hotmail.com",
        "password": "aaaaa",
    }

    target = "pypi_org.services.user_service.find_user_by_email"
    find_user = unittest.mock.patch(target, return_value=None)
    target = "pypi_org.services.user_service.create_user"
    create_user = unittest.mock.patch(target, return_value=User())
    request = flask_app.test_request_context(path="account/register", data=form_data)

    with find_user, create_user, request:
        # Act
        resp: flask.Response = register_post()

    # Assert
    assert resp.location == "/account"
