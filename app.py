from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date


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
    
class Award(db.Model):
    __tablename__ = "Award"

    awardId = db.Column(db.Integer(), primary_key=True)
    awardTitle = db.Column(db.String(300), nullable=False)
    awardDate = db.Column(db.Date, nullable=False)
    awardPhoto = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'Item {self.awardTitle}'
    
class Event(db.Model):
    __tablename__ = "Event"

    eventId = db.Column(db.Integer(), primary_key=True)
    eventTitle = db.Column(db.String(300), nullable=False)
    eventDate = db.Column(db.Date, nullable=False)
    eventPhoto = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'Item {self.eventTitle}'
    
class Programme(db.Model):
    progId = db.Column(db.Integer(), primary_key=True)
    progName = db.Column(db.String(1000))
    progOverview = db.Column(db.String(200))
    progDuration = db.Column(db.String(100))
    progCampus = db.Column(db.String(100))
    progIntake = db.Column(db.String(100))
    progReq = db.Column(db.String(200))
    progOutline = db.Column(db.String(1000))
    progCareer = db.Column(db.String(500))

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
def programme():
    return render_template("programme.html")

@app.route('/programme1')
def programme1():
    id = request.args.get('id')
    return render_template("programme1.html",content=id)

@app.route('/programme2')
def programme2():
    return render_template("programme2.html")

@app.route('/recognition')
def recognition():
    return render_template("recognition.html")

@app.route('/whyChooseUs')
def whyChooseUs():
    return render_template("whyChooseUs.html")

@app.route('/highlights/<int:page_num>', methods=['GET', 'POST'])
def highlights(page_num):
    if request.method == 'POST':
        awardYearInput = request.form.get('awardYear')

        if awardYearInput == '2023':
            start_date = date(2023, 1, 1)
            end_date = date(2023, 12, 31)
        elif awardYearInput == '2022':
            start_date = date(2022, 1, 1)
            end_date = date(2022, 12, 31)
        elif awardYearInput == '2021':
            start_date = date(2021, 1, 1)
            end_date = date(2021, 12, 31)
        elif awardYearInput == '2020':
            start_date = date(2020, 1, 1)
            end_date = date(2020, 12, 31) 
        else: 
            start_date = date(2020, 1, 1)
            end_date = date(2023, 12, 31)

        awardInputStartDate = start_date;
        awardInputEndDate = end_date;
        award = Award.query.filter(Award.awardDate.between(awardInputStartDate, awardInputEndDate)).paginate(per_page = 8, page = page_num, error_out = True)

    else:
        award = Award.query.paginate(per_page = 8, page = page_num, error_out = True)
    return render_template("highlights.html", awards=award)

@app.route('/events/<int:page_num>')
def events(page_num):
    if request.method == 'POST':
        eventYearInput = request.form.get('eventYear')

        if eventYearInput == '2023':
            start_date = date(2023, 1, 1)
            end_date = date(2023, 12, 31)
        elif eventYearInput == '2022':
            start_date = date(2022, 1, 1)
            end_date = date(2022, 12, 31)
        elif eventYearInput == '2021':
            start_date = date(2021, 1, 1)
            end_date = date(2021, 12, 31)
        else: 
            start_date = date(2021, 1, 1)
            end_date = date(2023, 12, 31)

        eventInputStartDate = start_date;
        eventInputEndDate = end_date;
        event = Event.query.filter(Event.eventDate.between(eventInputStartDate, eventInputEndDate)).paginate(per_page = 8, page = page_num, error_out = True)

    else:
        event = Event.query.paginate(per_page = 8, page = page_num, error_out = True)
    return render_template("events.html", events=event)

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

@app.route('/aboutUs')
def aboutUs():
    return render_template("aboutUs.html")

@app.route('/cictis')
def cictis():
    return render_template("cictis.html")

@app.route('/cdsa')
def cdsa():
    return render_template("cdsa.html")

@app.route('/cci')
def cci():
    return render_template("cci.html")

@app.route('/ciot')
def ciot():
    return render_template("ciot.html")

@app.route('/ccncs')
def ccncs():
    return render_template("ccncs.html")

@app.route('/cicrnd')
def cicrnd():
    return render_template("cicrnd.html")

if __name__ == "__name__":
    app.run(debug=True)


