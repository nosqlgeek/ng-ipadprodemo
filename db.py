from redis import Redis
import config

## DB config
host = config.REDIS_CFG["host"]
port = config.REDIS_CFG["port"]
pwd = config.REDIS_CFG["password"]

## Connection
redis = Redis(host=host, port=port, password=pwd, charset="utf-8", decode_responses=True)

