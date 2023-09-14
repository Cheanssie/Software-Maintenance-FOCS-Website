from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///FOCS.db"
db = SQLAlchemy(app)
app.app_context().push()

class staffDirectory(db.Model):
    __tablename__ = "staffDirectory"

    id = db.Column(db.Integer, primary_key=True)
    staffPhoto = db.Column(db.String(128), nullable=False)
    staffName = db.Column(db.String(128), nullable=False)
    staffPosition = db.Column(db.String(128), nullable=False)
    staffTitle = db.Column(db.String(128), nullable=False)
    staffFaculty = db.Column(db.String(128), nullable=False)
    staffEducation = db.Column(db.String(128), nullable=False)
    staffEmail = db.Column(db.String(128), nullable=False)
    staffMajor = db.Column(db.String(128), nullable=False)
    staffInterest = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{self.staffName}'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/facilities')
def facilities():
    return render_template("facilities.html")

@app.route('/staffDirectory/<int:page_num>', methods=['GET', 'POST'])
def staffDirectoryRoute(page_num):
  
  if request.method == 'POST':
    staffs = staffDirectory.query.filter(staffDirectory.staffName.contains(request.form['search'])).paginate(per_page = 2, page = page_num, error_out = True)

  else:
      staffs = staffDirectory.query.paginate(per_page = 2, page = page_num, error_out = True)
  return render_template("staffDirectory.html", staffs=staffs)

@app.route('/programme')
def programmes():
    return render_template("programme.html")

@app.route('/whyChooseUs')
def whyChooseUs():
    return render_template("whyChooseUs.html")

@app.route('/testimonials')
def testimonials():
    return render_template("testimonials.html")

@app.route('/collaborationPartners')
def collaborationPartners():
    return render_template("collaborationPartners.html")

@app.route('/externalExaminers')
def externalExaminers():
    return render_template("externalExaminers.html")

@app.route('/IEAPBachelorDegree')
def IEAPBachelorDegree():
    return render_template("IEAPBachelorDegree.html")

@app.route('/IEAPPostgraduate')
def IEAPPostgraduate():
    return render_template("IEAPPostgraduate.html")

if __name__ == "__name__":
    app.run(debug=True)


