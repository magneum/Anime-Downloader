import os
class Config(object):
    LOGGER = True
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    TOKEN = os.environ.get("TOKEN")
    LOAD =[]
class Development(Config):
    LOGGER = True
