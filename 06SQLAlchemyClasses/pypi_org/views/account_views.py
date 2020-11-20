import flask

blueprints = flask.Blueprint('account', __name__, template_folder="templates")


""" --------------- Account --------------- """
@blueprints.route('/account')
def index():
    return flask.render_template('account/index.html')


""" --------------- Register --------------- """
@blueprints.route('/account/register', methods=['GET'])
def register_get():
    return flask.render_template('account/register.html')

@blueprints.route('/account/register', methods=['POST'])
def register_post():
    return flask.render_template('account/register.html')


""" --------------- Login --------------- """
@blueprints.route('/account/login', methods=['GET'])
def login_get():
    return flask.render_template('account/login.html')

@blueprints.route('/account/login', methods=['POST'])
def login_post():
    return flask.render_template('accound/login.html')