flask_ssl_skeleton
==================

Skeleton project for flask + ssl + user login. This is a combination of examples from the interwebs for setting up SSL for flask and using Flask-Auth. 

Users
===============
This skeleton uses SQLite, Flask & Flask-Auth to do the dirty work of user login, password hashing,
salting etc.

User storage is up to you long term, this stores them in SQLite via SQLAlchemy. That's proabably not a good long term solution (at least not in my neck of the woods). Flask-Auth gives us a handy users class that has the ORM done for us, so hook it up to a real db if that works for you. 

Keys / crts are assumed to be on my laptop, you should change that. Signed, self signed, that's all up to you. The Flask code that matters the ssl_context bit in app.run(). It's down at the bottom of the file. This just sets up ssl for the development server, you still need to wire in your real webserver longterm. This just gets you going and pleases the "you didn't do ssl, you didn't do the hardwork" jokers.  
   
    ...
    ssl_context=('/your/path_to.crt', '/your/path_to.key')

The logic around redirecting logged in users is not solid and not worthy of a real app. That's not the intention here as this is a stating point. The comments in flask_ssl_skeleton.py attempts to call out things that aren't a great idea. Specifically, just because you're still logged in does not mean you're still a valid user. (i.e. your session token has not expired but someone booted you from the user db). Further evidence not to trust all the code you find on the internets.

Getting Started
===================
Setup a new 2.7 virtualenv

Install the requirements:
    
    pip install -r requirements.txt

Setup ssl keys, this is a good explination (method 2). Note he has a copy command and a generation command run together:

http://kracekumar.com/post/54437887454/ssl-for-flask-local-development

There's tests in tests/flask_ssl_skeleton_test.py, run them & study them to get a feel for how to test. 
Run the app and navigate to the URL.
Rename flask_ssl_skeleton.py to something more better for you.  
Change (or remove) <code>init_users</code> to load your users.

Follow the pattern set forth in <code>admin()</code> to have users be logged in.

Replace the way we find users in <code>index()</code> to be how you find a user in order to authenticate them.

Windows Notes
===================
Install open ssl from http://slproweb.com/products/Win32OpenSSL.html. Install the full version, not the lite version, make sure it's in your path. This appears to be a pain in the butt. Documentation on how to install pyOpenSSL may be of some assistance. Make sure you also install the VS 8 redistributables. 

If open ssl complains about not finding a config file at /usr/local/ssl/openssl.cnf
    
    set OPENSSL_CONFG=C:\OpenSSL-Win64\bin\openssl.cfg

Beware of file associations in windows. If you don't type python /your/script you'll use the file associations, which will NOT point to the python in your virtualenv. This will cause all maner of headache and confusion.

Other Notes
=================
PyCharm complains about flaskext not being found (in import statements). This does not seem to effect execution, but it
drives me crazy. I've run <code>touch site-packages/python2.7/flaskext/__init__.py</code> to silence this squiggly line.