from flask import Flask, request, redirect, session, url_for
from flask.ext.auth.auth import SESSION_USER_KEY, logout
from flaskext.auth import Auth, login_required
from flaskext.auth.models.sa import get_user_class
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from sqlalchemy.orm.exc import NoResultFound

Flask.get = lambda self, path: self.route(path, methods=['get'])
Flask.put = lambda self, path: self.route(path, methods=['put'])
Flask.post = lambda self, path: self.route(path, methods=['post'])
Flask.delete = lambda self, path: self.route(path, methods=['delete'])

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.secret_key = 'The debug secret.'
db = SQLAlchemy(app)
auth = Auth(app, login_url_name='index')
User = get_user_class(db.Model)


@login_required()
@app.get('/admin')
def admin():
    user_key = session.get(SESSION_USER_KEY)
    if not user_key:
        return redirect(url_for('index'))
    username = session.get(SESSION_USER_KEY)['username']
    app.logger.debug(username + " accessed /admin")
    return "Hello " + username

#TODO There is a not so small bug here. It's not safe to just check the users token as the users
# browser may still have one even if the user has been deleted from the database. Do something
# more better in a real implementation.
@app.get('/index')
@app.get('/')
def index():
    user_key = session.get(SESSION_USER_KEY)
    if user_key:
        username = user_key['username']
        app.logger.debug(username + " hit the root")
        return redirect(url_for('admin'))
    app.logger.debug('giving back login form')
    return mk_form("Log In")


@app.post('/')
def do_login():
    username = request.form['username']
    try:
        user = User.query.filter(User.username == username).one()
        if user is not None:
            if user.authenticate(request.form['password']):
                app.logger.debug(username + " logged in!")
                return redirect(url_for('admin'))
    except NoResultFound:
        pass

    return 'Failure to login'


@app.post('/users/create')
def do_create_user():
    username = request.form['username']
    if User.query.filter(User.username == username).first():
        return 'User already exists.'
    password = request.form['password']
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.get('/users/create')
def create_user():
    return mk_form("Create")


def mk_form(button_text):
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="%s"/>
            </form>
        ''' % button_text


def logout_view():
    user_data = logout()
    if user_data is None:
        return 'No user to log out.'
    return 'Logged out user {0}.'.format(user_data['username'])


if __name__ == '__main__':
    try:
        open('/tmp/flask_auth_test.db')
    except IOError:
        db.create_all()
        app.logger.info("Created db")
    app.run('0.0.0.0', debug=True,
            ssl_context=('/Users/jkruck/git/flask_ssl_skeleton/keys/server.crt',
                         '/Users/jkruck/git/flask_ssl_skeleton/keys/server.key'))