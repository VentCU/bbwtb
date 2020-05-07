import argparse
import os

from flask import Flask

app = Flask(__name__)

from app import routes

