from flask import Flask, flash, redirect, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import os
import difflib
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///FOCS.db"
db = SQLAlchemy(app)
app.app_context().push()

#change the folder name 
imageUploadPath = os.path.join(os.getcwd(), 'static', 'assets', 'img', 'uploadImageFolder')

app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = imageUploadPath
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

imageAllowedExtension = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in imageAllowedExtension

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

def __init__(self, progName, progOverview, progDuration, progCampus, progIntake, progReq, progOutline, progCareer):
    self.progName = progName
    self.progOverview = progOverview
    self.progDuration = progDuration
    self.progCampus = progCampus
    self.progIntake = progIntake
    self.progReq = progReq
    self.progOutline = progOutline
    self.progCareer = progCareer


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
    return render_template("programme1.html",progs = Programme.query.filter_by(progId = id).all())

@app.route('/programme2')
def programme2():
    id = request.args.get('id')
    return render_template("programme2.html",progs = Programme.query.filter_by(progId = id).all())

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

@app.route('/events/<int:page_num>', methods=['GET', 'POST'])
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

@app.route('/enrollment')
def enrollment():
    return render_template("enrollment.html")

@app.route('/viewRecords')
def viewRecords():
    records = staffDirectory.query.all()
    return render_template('viewRecords.html', records=records)

@app.route('/uploadResult')
def uploadResult():
    return render_template("uploadResult.html", os=os) 

def readImage(filename):
    myconfig = r"--psm 4 --oem 3"
    #change image path name
    uploadImage = Image.open(f'{imageUploadPath}/{filename}')
    text = pytesseract.image_to_string(uploadImage, config=myconfig)
    print(text)
    return correctText(text)

#build a grade dictionary
grade_dict = {
    "CEMERLANG TERTINGGI": "A+",
    "CEMERLANG TINGGI": "A",
    "CEMERLANG": "A-",
    "KEPUJIAN TERTINGGI": "B+",
    "KEPUJIAN TINGGI": "B",
    "KEPUJIAN ATAS": "C+",
    "KEPUJIAN": "C",
    "LULUS ATAS": "D",
    "LULUS": "E",
    "GAGAL": "G",
    "TIDAK HADIR": "TH"
}

#build a common word dictionary
common_words = ["1103", "1119", "1225", "1249", "1449", "1511", 
                "2215", "2361", "3472", "3756", "3766", "3767",
                "4531", "4541", "4551", "4561", "2205", "6351",
                "5227", "5228", "2361",
                "BAHASA", "MELAYU", "INGGERIS", "PENDIDIKAN", "MORAL",
                "SEJARAH", "MATHEMATICS", "ADDITIONAL", "PHYSICS",
                "CHEMISTRY", "BIOLOGY", "CINA", "PRINSIP", "PERAKAUNAN", 
                "CEMERLANG", "TERTINGGI", "TINGGI", "KEPUJIAN", 
                "KESUSASTERAAN","KOMUNIKATIF", "PERNIAGAAN", "EKONOMI",
                "AL-QURAN", "DAN", "ISLAMIAH", "SYARI'AH", "ISLAMIAH",
                "ARAB"]
                
# Create a list of subjects
subjects = ["BAHASA MELAYU", 
            "BAHASA INGGERIS", 
            "PENDIDIKAN MORAL", 
            "SEJARAH", 
            "MATHEMATICS", 
            "ADDITIONAL MATHEMATICS", 
            "PHYSICS", 
            "CHEMISTRY", 
            "BIOLOGY", 
            "BAHASA CINA", 
            "PRINSIP PERAKAUNAN"]

# Create a dictionary to map subject codes to subject names
subject_codes = {
    "1103": "BAHASA MELAYU",
    "1119": "BAHASA INGGERIS",
    "1225": "PENDIDIKAN MORAL",
    "1249": "SEJARAH",
    "1449": "MATHEMATICS",
    "3472": "ADDITIONAL MATHEMATICS",
    "4531": "PHYSICS",
    "4541": "CHEMISTRY",
    "4551": "BIOLOGY",
    "6351": "BAHASA CINA",
    "3756": "PRINSIP PERAKAUNAN",
}

def correctText(text):
    corrected_input = correct_input(text, common_words)
    print(corrected_input)
    subject_grade_dict = {}
    # Iterate over the list of subjects
    for subject in subjects:
        # Check if the subject is present in the input text
        if subject in corrected_input or subject_codes[subject] in corrected_input:
            # Find the grade for the subject
            grade = re.search(r"CEMERLANG TERTINGGI|CEMERLANG TINGGI|CEMERLANG|KEPUJIAN TERTINGGI|KEPUJIAN TINGGI|KEPUJIAN ATAS|KEPUJIAN|LULUS ATAS|LULUS|GAGAL|TIDAK HADIR", corrected_input).group()

            # Print the grade for the subject
            subject_grade_dict[subject] = grade_dict[grade]
            #print(f"{subject} : {grade_dict[grade]}")
    
    return subject_grade_dict


def compare_words(word1, word2):
  # Calculate the similarity score between the two words using the difflib.SequenceMatcher() function
  similarity_score = difflib.SequenceMatcher(None, word1, word2).ratio()
  
  # Return the similarity score
  return similarity_score

def correct_input(user_input, common_words):
    # Split the OCR-captured text by lines
    lines = user_input.split("\n")

    # For each line, split by the words by spaces
    corrected_lines = []
    for line in lines:
        words = line.split(" ")

        # For each word, compare it with each common word in the list
        corrected_words = []
        for word in words:

            # Calculate the similarity score between the word and each common word
            similarity_score = 0
            common_word = None
            for common_word in common_words:
                similarity_score = compare_words(word, common_word)
                
                # If the similarity score is greater than 0.8, then the word is considered to be correct.
                if similarity_score > 0.8:
                    corrected_words.append(common_word)
        
        # Add the corrected words to the corrected_lines list
        corrected_lines.append(" ".join(corrected_words))
    
    # Return the corrected_lines list
    return "\n".join(corrected_lines)


#flash - show message to users
@app.route('/uploadResult', methods=['POST', 'GET'])
def upload_image():
    if request.method == "POST":
        if 'resultInputfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        inputFile = request.files['resultInputfile']
        if inputFile.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if inputFile and allowed_file(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            readResults = dict(readImage(filename))
            print(readResults)
            return render_template("extractResult.html", filename=filename, readResults=readResults)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url) 
        
    else:
        return render_template("uploadResult.html")
    
@app.route('/process_ocr', methods=['POST'])
def process_ocr():
   if 'file' not in request.files:
       return jsonify({'error':'No file apart'})
   
   file = request.files['file']
   
   if file.filename == '':
        return jsonify({"error": "No selected file"})
   
   if file:
        filename = secure_filename(file.filename)
        file_path = f'{imageUploadPath}/{filename}'
        file.save(filename)

        readResults = readImage(filename)
        os.remove(filename)  # Remove the uploaded file
        
        return jsonify(readResults)

if __name__ == "__name__":
    app.run(debug=True)


