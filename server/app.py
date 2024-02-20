from ..matcher.core.match import Matcher
from flask import Flask, url_for
print(__package__)
app = Flask(__name__, static_folder="../static")
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/match")
def match():
    matcher = Matcher("foo")
    best_match_path, best_match_similarity = matcher.match("home.jpg")
    return url_for("static", filename=f"{best_match_path}.jpg", _external=False) + f" similarity: {best_match_similarity}"

if __name__ == "__main__":
    app.run("localhost", 5000, True)