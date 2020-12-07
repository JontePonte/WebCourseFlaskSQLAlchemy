
import os
import sys

import unittest.mock

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel
from pypi_org.viewmodels.account.login_viewmodel import LoginViewModel
from pypi_org.data.users import User
from test_client import flask_app


def test_example():
    print("Test example...")
    assert 1 + 2 == 3


""" -------------------- Login ----------------------- """


def test_login_validation_when_valid():
    # Arrange
    form_data = {
        'email': 'john_nordstrand@hotmail.com',
        'password': 'aaaaa'
    }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = LoginViewModel()

    # Act
    vm.validate()

    # Assert
    assert vm.error is None


def test_login_validation_when_no_email():
    # Arrange
    form_data = {
        'email': ' ',
        'password': 'aaaaa'
    }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = LoginViewModel()

    # Act
    vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify a email' in vm.error


def test_login_validation_when_no_password():
    # Arrange
    form_data = {
        'email': 'john_nordstrand@hotmail.com',
        'password': ''
    }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = LoginViewModel()

    # Act
    vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify a password' in vm.error


""" -------------------- Register ----------------------- """


def test_register_validation_when_valid():
    # Arrange
    form_data = {
        'name': 'John',
        'email': 'john_nordstrand@hotail.com',
        'password': 'aaaaa'
        }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is None


def test_register_validation_when_email_exist():
    # Arrange
    form_data = {
        'name': 'John',
        'email': 'john_nordstrand@hotail.com',
        'password': 'aaaaa'
        }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    user = User()
    user.name = 'John'
    user.email = 'john_nordstrand@hotmail.com'
    with unittest.mock.patch(target, return_value=user):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'email already exists' in vm.error


def test_register_validation_when_no_email():
    # Arrange
    form_data = {
        'name': 'John',
        'email': '',
        'password': 'aaaaa'
        }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify a email' in vm.error


def test_register_validation_when_no_password():
    # Arrange
    form_data = {
        'name': 'John',
        'email': 'john_nordstrand@hotmail.com',
        'password': ' '
        }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify a password' in vm.error


def test_register_validation_when_short_password():
    # Arrange
    form_data = {
        'name': 'John',
        'email': 'john_nordstrand@hotmail.com',
        'password': 'aaaa'
        }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'Password needs' in vm.error


def test_register_validation_when_no_name():
    # Arrange
    form_data = {
        'name': ' ',
        'email': 'john_nordstrand@hotmail.com',
        'password': 'aaaaa'
        }

    with flask_app.test_request_context(path='account/register', data=form_data):
        vm = RegisterViewModel()

    # Act
    target = 'pypi_org.services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'specify a name' in vm.error
