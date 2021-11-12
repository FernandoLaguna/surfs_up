import pandas as pd

from flask import Flask
apps = Flask(__name__)
@apps.route('/')
def hola_mundo():
    return "Hola mundo"