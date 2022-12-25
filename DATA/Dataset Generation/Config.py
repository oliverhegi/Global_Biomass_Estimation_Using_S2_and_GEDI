# Configure SentinelHub
from sentinelhub import SHConfig

config = SHConfig()

# Enter user id and secret code below
# Account for SentinelHub API can be created here https://www.sentinel-hub.com/develop/api/
config.instance_id = '' 
config.sh_client_id = ''
config.sh_client_secret = ''

config.save()    
