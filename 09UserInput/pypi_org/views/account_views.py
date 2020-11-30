import flask

import pypi_org.services.user_service as user_service

blueprint = flask.Blueprint('account', __name__, template_folder="templates")


""" --------------- Account --------------- """


@blueprint.route('/account')
def index():
    return flask.render_template('account/index.html')


""" --------------- Register --------------- """


@blueprint.route('/account/register', methods=['GET'])
def register_get():
    return flask.render_template('account/register.html')


@blueprint.route('/account/register', methods=['POST'])
def register_post():
    r = flask.request

    name = r.form.get('name', '')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not name or not email or not password:
        return flask.render_template(
            'account/register.html',
            name=name,
            email=email,
            password=password,
            error="Some required fields are missing.",
            )
    # TOTO: Create the user
    user = user_service.create_user(name, email, password)
    if not user:
        return flask.render_template(
            'account/register.html',
            name=name,
            email=email,
            password=password,
            error="A user with that email already exists.",
            )
    # Log in browser as a session
    return flask.redirect('/account')


""" --------------- Login --------------- """


@blueprint.route('/account/login', methods=['GET'])
def login_get():
    return flask.render_template('account/login.html')


@blueprint.route('/account/login', methods=['POST'])
def login_post():
    r = flask.request

    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not email or not password:
        return flask.render_template(
            'account/login.html',
            email=email,
            password=password,
            error="Please enter email and password.",
            )

    user = user_service.login_user(email, password)
    if not user:
        return flask.render_template(
            'account/login.html',
            email=email,
            password=password,
            error="The account does not exist or the password is wrong.",
            )
    # Log in browser as a session
    return flask.redirect('/account')
