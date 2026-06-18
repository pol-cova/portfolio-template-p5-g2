from datetime import datetime

from flask import Flask, render_template

from app.data import (
    profile,
    about_paragraphs,
    marquee_items,
    experiences,
    education,
    hobbies,
    trips,
)

app = Flask(__name__)

nav_links = [
    {"label": "Home", "href": "/"},
    {"label": "Experience", "href": "/experience"},
    {"label": "Education", "href": "/education"},
    {"label": "Hobbies", "href": "/hobbies"},
    {"label": "Travel", "href": "/travel"},
]


@app.context_processor
def inject_globals():
    """Makes these available in every template without passing explicitly."""
    return {
        "profile": profile,
        "nav_links": nav_links,
        "current_year": datetime.now().year,
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        about_paragraphs=about_paragraphs,
        marquee_items=marquee_items,
    )


@app.route("/experience")
def experience():
    return render_template("experience.html", experiences=experiences)

@app.route("/education")
def education_page():
    return render_template("education.html", education=education)

@app.route("/hobbies")
def hobbies_page():
    return render_template("hobbies.html", hobbies=hobbies)


@app.route("/travel")
def travel():
    return render_template("travel.html", trips=trips)

if __name__ == "__main__":
    app.run(debug=True)
