from flask import Flask, render_template, request, redirect
from flask_babel import Babel, _
import sqlite3
from sentiment import get_sentiment

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

from flask_babel import get_locale as babel_get_locale

def get_locale():
    return request.args.get('lang') or 'en'

babel.locale_selector_func = get_locale

@app.context_processor
def inject_globals():
    return dict(_=_, get_locale=get_locale)


def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS feedback
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT,
         product_id TEXT,
         rating INTEGER,
         text TEXT,
         sentiment REAL,
         points INTEGER)''')
    conn.close()

@app.route("/")
def home():
    return _("QR-AI Feedback System")

@app.route("/feedback")
def feedback():
    product_id = request.args.get("product_id")
    return render_template("feedback.html", product_id=product_id)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    rating = int(request.form["rating"])
    text = request.form["text"]
    product_id = request.form["product_id"]
    sentiment = get_sentiment(text)
    points = 5

    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO feedback (name, product_id, rating, text, sentiment, points) VALUES (?, ?, ?, ?, ?, ?)",
                 (name, product_id, rating, text, sentiment, points))
    conn.commit()
    conn.close()
    return _("Thanks for your feedback!")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, COUNT(*), AVG(sentiment) FROM feedback GROUP BY product_id")
    data = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", data=data)

init_db()

if __name__ == "__main__":
    app.run(debug=True)
