from flask import Flask

from updater import run_updater_thread


run_updater_thread()

app = Flask(__name__)

@app.route("/")
def main():
    return "It works"
