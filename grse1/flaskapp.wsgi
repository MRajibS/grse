#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/grse1/grse1/")

from main_app import app as application
application.secret_key = 'TestSecretKey'

