from flask import Flask, g, request, redirect, session
from flask.ext.auth.auth import SESSION_USER_KEY
from flaskext.auth import Auth, AuthUser, login_required

app = Flask(__name__)
auth = Auth(app)

@app.before_request
def init_users():
    admin_user = AuthUser(username='admin')
    admin_user.set_and_encrypt_password('password')
    g.users = {'admin': admin_user}


@app.route('/admin')
@login_required()
def admin():
    return "Hello Admin " + str(session.get(SESSION_USER_KEY, None))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if username in g.users:
            # Authenticate and log in!
            if g.users[username].authenticate(request.form['password']):
                return redirect('/admin')
        return 'Failure :('
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="Log in"/>
            </form>
        '''

if __name__ == '__main__':
    app.secret_key = 'The debug secret.'
    app.run('0.0.0.0', debug=True,
            ssl_context=('/Users/jkruck/git/flask_ssl_skeleton/keys/server.crt',
                         '/Users/jkruck/git/flask_ssl_skeleton/keys/server.key'))
