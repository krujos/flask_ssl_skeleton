flask_ssl_skeleton
==================

Skeleton project for flask + ssl + user login. This is a combination of examples from the interwebs for setting up SSL for flask and using Flask-Auth. 

Uses Flask & Flask-Auth to do the dirty work
User storage is up to you, this just stores them in memory in the app

	TODO Put it in sqlalchemy user class or something. 

Keys / crts are assumed to be on my laptop, you should change that.
   
    ...
    ssl_context=('/your/path_to.crt', '/your/path_to.key')
   
Getting Started
===================
Install the requirements 
    
		pip install -f requirements.txt

Change (or remove) <code>init_users</code> to load your users

Follow the pattern set forth in <code>admin()</code> to have users be logged in. It is importent that <code>@login_required</code> is the decorator closest to the function (bottom most). Otherwise it won't work and anyone can hit the endpoint. 


Replace the way we find users in <code>index()</code> to be how you find a user in order to authenticate them.
