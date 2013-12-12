from flask import Flask, request, redirect, session, url_for
from flask.ext.auth.auth import SESSION_USER_KEY, logout
from flaskext.auth import Auth, login_required
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from sqlalchemy.orm.exc import NoResultFound

Flask.get = lambda self, path: self.route(path, methods=['get'])
Flask.put = lambda self, path: self.route(path, methods=['put'])
Flask.post = lambda self, path: self.route(path, methods=['post'])
Flask.delete = lambda self, path: self.route(path, methods=['delete'])
from flaskext.auth.models.sa import get_user_class

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
auth = Auth(app, login_url_name='index')

User = get_user_class(db.Model)


@app.get('/admin')
@login_required()
def admin():
    username = session.get(SESSION_USER_KEY, None)['username']
    app.logger.debug(username + " accessed /admin")
    return "Hello " + username

@app.get('/')
def index():
    user_key = session.get(SESSION_USER_KEY, None)
    if user_key:
        username = user_key['username']
        app.logger.debug(username + " hit the root")
        return redirect('admin')

    app.logger.debug('giving back login form')
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="Log in"/>
            </form>
        '''

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
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="Create"/>
            </form>
        '''


def logout_view():
    user_data = logout()
    if user_data is None:
        return 'No user to log out.'
    return 'Logged out user {0}.'.format(user_data['username'])

if __name__ == '__main__':
    app.secret_key = 'The debug secret.'
    app.run('0.0.0.0', debug=True,
            ssl_context=('/Users/jkruck/git/flask_ssl_skeleton/keys/server.crt',
                         '/Users/jkruck/git/flask_ssl_skeleton/keys/server.key'))
