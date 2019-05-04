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
host = config.REDIS_CFG['host']
port = config.REDIS_CFG['port']
pwd = config.REDIS_CFG['password']

redis = Redis(host=host, port=port, password=pwd, charset="utf-8", decode_responses=True)

## Warning: Only for testing purposes!
#redis.flushdb();

## Test DB config
redis.set("test", "Database connectivity works as expected!");

## Routes
@app.route("/db/test")
def dbtest():
	status = redis.get("test")
	return render_template('dbtest.html', status=status)

@app.route("/db/exec")
def execcmd():
	cmd=request.args.get('cmd')
	
	if (cmd != None):
		print("Trying to execute: {}".format(cmd))
		try:
			result = redis.execute_command(cmd)
			status = "Success"
			return render_template('execcmd.html', status=status, result=result)
		except RedisError as err:
			error = err
			return render_template('execcmd.html', error=err)
	
	return render_template('execcmd.html')

@app.route("/")
def root():
	return redirect('/db/exec')
 
    
if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0', port=5000)
