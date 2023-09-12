from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/facilities')
def facilities():
    return render_template("facilities.html")

@app.route('/staffDirectory')
def staffDirectory():
    return render_template("staffDirectory.html")

@app.route('/programme')
def programmes():
    return render_template("programme.html")

if __name__ == "__name__":
    app.run(debug=True)


