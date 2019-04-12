#!/usr/bin/env python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/catalog/")
sys.path.insert(0, "/var/www/html/catalog/wsgi/")
from main import app as application
