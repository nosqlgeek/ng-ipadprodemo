print("Starting Hello World service ....");

# Imports
from flask import Flask
from redis import Redis
import config

## Init
app = Flask(__name__)


## DB config
host = config.REDIS_CFG['host']
port = config.REDIS_CFG['port']
pwd = config.REDIS_CFG['password']

redis = Redis(host=host, port=port, password=pwd)

## Warning: Only for testing purposes!
#redis.flushdb();

## Test DB config
redis.set("test", "Database connectivity works as expected!");

## Routes
@app.route("/test/db")
def hello():
	res = redis.get("test")
	return res
    
## TODO: Add additional routes!    
    
    
if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0', port=5000)
