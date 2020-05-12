from flask import Flask, request, url_for, jsonify, make_response, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*')

from .router import *
