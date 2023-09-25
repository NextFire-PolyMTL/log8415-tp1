import os

from flask import Flask

INSTANCE_NUMBER = os.environ.get("INSTANCE_NUMBER", "unknown")

app = Flask(__name__)


@app.route("/")
def hello_world():
    return f"Instance number {INSTANCE_NUMBER} is responding now!"
