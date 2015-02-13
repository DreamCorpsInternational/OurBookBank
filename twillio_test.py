import logging
import sys
from configparser import ConfigParser
import os

config = ConfigParser()
config.readfp(open("obb.cfg"))

# Twillio call.
targetURI = config.get("twillioCredentials", "targetURI")
fromNumber = config.get("twillioCredentials", "fromNumber")
baCredentials = config.get("twillioCredentials", "basicAuthCredentials")

body = "bla bla"
toNumber = "+6473093872"

curlCommand = "curl -X POST '" + targetURI + "' -d 'From=" + fromNumber + "' -d 'To=" + toNumber + "' -d 'Body=" + body + "' -u " + baCredentials

print curlCommand
os.system(curlCommand)
