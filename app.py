print("Starting the web application ....");

# Imports
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from redis import Redis
from redis.exceptions import RedisError
import config

## Init
app = Flask(__name__)


## DB config
host = config.REDIS_CFG["host"]
port = config.REDIS_CFG["port"]
pwd = config.REDIS_CFG["password"]

redis = Redis(host=host, port=port, password=pwd, charset="utf-8", decode_responses=True)

## Warning: Only for testing purposes!
#redis.flushdb();

## Routes
@app.route("/home")
def home():
	# View constants
	TITLE="Home"
	DESC="Welcome to this simple Redis demo application. This application allows you to check the database connectivity, access some database configuration details and to execute Redis commands."
	return render_template('home.html', title=TITLE, desc=DESC)

@app.route("/db/info")
def dbinfo():
	# View constants
	TITLE="Database Info"
	DESC="Some database details ..."
	
	items = []
	
	try:
		result = redis.info()
		#print(status)
		for k in result:
			item = {}
			item["key"] = k
			item["value"] = result[k]
			items.append(item)   
	except RedisError as err:
		item = {}
		item["key"] = "error"
		item["value"] = err
		items.append(item) 
	
	return render_template('dbinfo.html', title=TITLE, desc=DESC, items=items)

@app.route("/db/test")
def dbtest():
	# View constants
	TITLE="Test Connectivity"
	DESC="Find the status of the connectivity test below ..."
	
	status = "Not connected!"
	
	try:
		redis.set("db:test", "Database connectivity works as expected!");
		status = redis.get("db:test")
	except RedisError as err:
		status = err
	
	return render_template('dbtest.html', title=TITLE, desc=DESC, status=status)

@app.route("/db/exec")
def execcmd():
	# View constants
	TITLE="Execute Command"
	DESC="Just enter a command in the text field below ..."
	
	# Request params
	cmd=request.args.get("cmd")
	
	if (cmd != None):
		print("Trying to execute: {}".format(cmd))
		try:
			result = redis.execute_command(cmd)
			status = "Success"
			return render_template('execcmd.html', title=TITLE, desc=DESC, cmd=cmd, status=status, result=result)
		except RedisError as err:
			return render_template('execcmd.html', title=TITLE, desc=DESC, cmd=cmd, error=err)
	
	return render_template('execcmd.html', title=TITLE, desc=DESC)

@app.route("/")
def root():
	return redirect('/home')
 
    
if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0', port=5000)
