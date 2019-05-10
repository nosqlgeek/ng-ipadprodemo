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

### Home page
@app.route("/home")
def home():
	# View constants
	TITLE="Home"
	DESC="Welcome to this simple Redis demo application. This application allows you to check the database connectivity, access some database configuration details and to execute Redis commands."
	return render_template('home.html', title=TITLE, desc=DESC)

### Database info
@app.route("/db/info")
def dbinfo():
	# View constants
	TITLE="Database Info"
	DESC="Some database details ..."
	
	items = []
	
	try:
		result = redis.info()
		for k in result:
			item = {}
			item["key"] = k
			item["value"] = result[k]
			items.append(item)
		return render_template('dbinfo.html', title=TITLE, desc=DESC, items=items, status="Success")   
	except RedisError as err:
		return render_template('dbinfo.html', title=TITLE, desc=DESC, error=err) 

### Test connection
@app.route("/db/test")
def dbtest():
	# View constants
	TITLE="Test Connectivity"
	DESC="Find the status of the connectivity test below ..."
	
	try:
		redis.set("db:test", "Database connectivity works as expected!");
		status = redis.get("db:test")
		return render_template('dbtest.html', title=TITLE, desc=DESC, status=status)
	except RedisError as err:
		return render_template('dbtest.html', title=TITLE, desc=DESC, error=err)
	
### Execute a command
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
			
			# Nicer result output
			lines=[]
			if (isinstance(result, list)):
				# Adding this block for SCAN which returns the cursor followed by a list
				if len(result) == 2 and isinstance(result[1],list):
					lines = result[1]
					lines.insert(0, result[0])
				else:
					# Output of a list, i.e. KEYS *
					lines=result;
			elif (isinstance(result, dict)):
				# Adding support for a dict result (i.e. INFO)
				for k in result:
					val = "{} : {}".format(k, result[k])
					lines.append(val)
			else:
				# Everything else is just defaulting to a String output
				lines = str(result).splitlines()
		
			return render_template('execcmd.html', title=TITLE, desc=DESC, cmd=cmd, status='Success', lines=lines)
		except RedisError as err:
			return render_template('execcmd.html', title=TITLE, desc=DESC, cmd=cmd, error=err)
	
	return render_template('execcmd.html', title=TITLE, desc=DESC)

### Start page
@app.route("/")
def root():
	return redirect('/home')
 
    
if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0', port=5000)
