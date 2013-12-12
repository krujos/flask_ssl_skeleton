from flask import Flask, g, request, redirect, session
from flask.ext.auth.auth import SESSION_USER_KEY
from flaskext.auth import Auth, AuthUser, login_required
import logging


Flask.get = lambda self, path: self.route(path, methods=['get'])
Flask.put = lambda self, path: self.route(path, methods=['put'])
Flask.post = lambda self, path: self.route(path, methods=['post'])
Flask.delete = lambda self, path: self.route(path, methods=['delete'])

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
auth = Auth(app)

@app.before_request
def init_users():
    admin_user = AuthUser(username='admin')
    admin_user.set_and_encrypt_password('password')
    g.users = {'admin': admin_user}


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
        app.logger.debug(user_key['username'] + " hit the root")
        return redirect('/admin')

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
    if username in g.users:
        # Authenticate and log in!
        if g.users[username].authenticate(request.form['password']):
            app.logger.debug(username + " logged in!")
            return redirect('/admin')
    return 'Failure :('


if __name__ == '__main__':
    app.secret_key = 'The debug secret.'
    app.run('0.0.0.0', debug=True,
            ssl_context=('/Users/jkruck/git/flask_ssl_skeleton/keys/server.crt',
                         '/Users/jkruck/git/flask_ssl_skeleton/keys/server.key'))
