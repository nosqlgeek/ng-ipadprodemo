import uuid
from flask import Blueprint
from functools import wraps
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import redis

## Constants
TITLE="Login"
DESC="You need to be authenticated before you can execute commands."

## Helpers
def validate_session():
	result = False
	user = request.cookies.get("user")
	userSn = request.cookies.get("userSn")
	key = "{}:{}".format(user, "sn")
	session = redis.get(key)
	if session == userSn:
		result = True
	return result
	
### There is a logout happening if an error happens
def invalidate_session():
	user = request.cookies.get("user")
	userSn = request.cookies.get("userSn")
	key = "{}:{}".format(user, "sn")
	redis.delete(key)

	
def login_required(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		if not validate_session():
			return redirect('/login?redirect=true')
		else:
			return fn(*args, **kwargs)
	return wrapper
		
	
## Routes
login_page = Blueprint('login_page', __name__,template_folder='templates')


### Login page
@login_page.route("/login", methods=['GET', 'POST'])
def login():		
	# Handle the POST request
	if request.method == "POST":
		user = "redwc:user:{}".format(request.form.get('user'))
		password = request.form.get('password')
		create = request.form.get('create')
		
		error = None
		status = None
		
		# Create user
		if create == "on":
			exists = redis.get(user)
			
			if exists is not None:
				error = "User is already existing!"
			else:
				hash = generate_password_hash(password)
				redis.set(user, hash)
				status="User was successfully created."
		else:
			# Authenticate
		  print("Trying to authenticate ...")
		  hash = redis.get(user)
		  
		  if hash is None:
		  	error = "User not found!"
		  else:
		  	auth = check_password_hash(hash, password)
		  	if auth == True:
		  		status = "Successfully authenticated"
		  	else:
		  		error = "Authentication failed!"
		    				
		if error is not None:
			invalidate_session()
			return render_template('login.html', title=TITLE, desc=DESC, error=error)
		else:
			# Generate a session cookie
			session = str(uuid.uuid1());
			redis.set("{}:{}".format(user, "sn"), session)
			resp = make_response(render_template('login.html', title=TITLE, desc=DESC, status=status))
			resp.set_cookie("user", user)
			resp.set_cookie("userSn", session)
			return resp
	else:
		# Otherwise just show the login form
		if validate_session():
			return render_template('login.html', title=TITLE, desc=DESC, status="You are already logged in")
		elif request.args.get("redirect") == "true":
			return render_template('login.html', title=TITLE, desc=DESC, error="Login required!")
		else:
			return render_template('login.html', title=TITLE, desc=DESC)
			
	
