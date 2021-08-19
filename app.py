#!/usr/bin/env python3
from src import webapp
import os

PORT = os.getenv('PORT', 5000)
HOST = os.getenv('HOST', '0.0.0.0')

if __name__ == '__main__':
    webapp.run(host=HOST, port=PORT, debug=True)
