print("Starting Hello World service ....");

# Imports
from flask import Flask
from redis import Redis

## Init
app = Flask(__name__)

## TODO: Read password from JSON file
redis = Redis(host='redis-18210.c12.us-east-1-4.ec2.cloud.redislabs.com', port=18210, password='49FSIbUuXjoFzC5tzM2k1METm2r3vBsK')

## Test
redis.set("hello", "Hello World again!");

## Routes
@app.route("/hello")
def hello():
	res = redis.get("hello")
	return res
    
if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0', port=5000)
