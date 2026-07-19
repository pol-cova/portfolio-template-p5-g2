import os
import re
import hashlib
from datetime import datetime

import yaml
from flask import Flask, render_template, request
from peewee import CharField, DateTimeField, Model, MySQLDatabase, SqliteDatabase, TextField
from playhouse.shortcuts import model_to_dict


app = Flask(__name__)
app.config["FLASK_DEBUG"] = os.environ.get("FLASK_DEBUG", 0)

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

@app.template_filter("gravatar_hash")
def gravatar_hash(email):
    normalized_email = (email or "").strip().lower().encode("utf-8")
    return hashlib.md5(normalized_email).hexdigest()

if os.environ.get("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase(":memory:")
else:
    mydb = MySQLDatabase(
        os.environ.get("MYSQL_DATABASE"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        host=os.environ.get("MYSQL_HOST"),
        port=3306,
    )

# timeline schema
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.context_processor
def inject_globals():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "data.yml"), "r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    return {
        **data,
        "current_year": datetime.now().year,
    }


# api routes
@app.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")

    if not name:
        return "Invalid name", 400
    if not content:
        return "Invalid content", 400
    if not email or not EMAIL_RE.fullmatch(email):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    if request.headers.get("HX-Request"):
        return render_template("partials/_timeline_posts.html", posts=[timeline_post])

    return model_to_dict(timeline_post)

@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

# delete rute (for the curl test)
@app.route("/api/timeline_post/<int:id>", methods=["DELETE"])
def delete_timeline_post(id):
    q = TimelinePost.delete().where(getattr(TimelinePost, 'id') == id)
    res = q.execute()

    if res == 0:
        return {"error": "Not found"}, 404

    return {"message": "Post deleted Successfully"}, 204

@app.route("/api/timeline_post", methods=["DELETE"])
def delete_timeline_posts_by_name():
    name = request.form.get("name")
    if name:
        TimelinePost.delete().where(TimelinePost.name == name).execute()
        return {"message": f"Deleted posts by {name}"}, 200
    return {"error": "Missing name"}, 400

# web routes
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

@app.route("/timeline")
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template("timeline.html", posts=posts)


if __name__ == "__main__":
    app.run()
