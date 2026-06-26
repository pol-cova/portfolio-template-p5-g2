import os
from datetime import datetime

import yaml
from flask import Flask, render_template

app = Flask(__name__)
app.config["FLASK_DEBUG"] = os.environ.get("FLASK_DEBUG", 0)


@app.context_processor
def inject_globals():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "data.yml"), "r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    return {
        **data,
        "current_year": datetime.now().year,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/experience")
def experience():
    return render_template("experience.html")


@app.route("/education")
def education_page():
    return render_template("education.html")


@app.route("/hobbies")
def hobbies_page():
    return render_template("hobbies.html")


@app.route("/travel")
def travel():
    return render_template("travel.html")


@app.route("/apps")
def apps_page():
    return render_template("apps.html")


if __name__ == "__main__":
    app.run()
