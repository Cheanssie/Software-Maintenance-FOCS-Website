from flask import Flask, flash, redirect, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence, Integer
from datetime import date, datetime
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import os
import difflib
import re
import socket
import uuid
from ua_parser import user_agent_parser
import pprint
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///FOCS.db"
db = SQLAlchemy(app)
app.app_context().push()

#change the folder name 
imageUploadPath = os.path.join(os.getcwd(), 'static', 'assets', 'img', 'uploadImageFolder')

app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = imageUploadPath
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hardcorestore888@gmail.com'
app.config['MAIL_PASSWORD'] = 'ommmtwibyfgqtqdf'
mail = Mail(app)
socketio = SocketIO(app)

imageAllowedExtension = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in imageAllowedExtension

class ChatMessage(db.Model):
    __tablename__ = "Message"

    msgId = db.Column(Integer, Sequence('msg_id_seq'), primary_key=True)
    time = db.Column(db.String(128), nullable=False)
    date = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    sender = db.Column(db.String(128), nullable=False)
    requestId = db.Column(db.String(128), nullable=False)

class EnquiryRequest(db.Model):
    __tablename__ = "EnquiryRequest"

    chatId = db.Column(db.String(128), primary_key=True)
    chatTitle = db.Column(db.String(128), nullable=False)
    chatDetails = db.Column(db.String(500), nullable=False)
    userName = db.Column(db.String(128), nullable=False)
    userEmail = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, nullable=False)


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
    
class Academician(db.Model):
    __tablename__="Academician"

    acaId = db.Column(db.Integer, primary_key=True)
    acaName = db.Column(db.String(128))
    acaPosition = db.Column(db.String(256))
    acaProg = db.Column(db.String(256))
    acaMajor = db.Column(db.String(128))
    acaAoi = db.Column(db.String(256))
    acaBio = db.Column(db.String(2048))
    acaPic = db.Column(db.String(128))
    acaEmail = db.Column (db.String(128))
    def __repr__(self):
        return f'Item {self.acaName}'
    
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
    progCategory = db.Column(db.String(100))

    def __repr__(self):
        return f'Item {self.progName}'

def __init__(self, progName, progOverview, progDuration, progCampus, progIntake, progReq, progOutline, progCareer, progCategory):
    self.progName = progName
    self.progOverview = progOverview
    self.progDuration = progDuration
    self.progCampus = progCampus
    self.progIntake = progIntake
    self.progReq = progReq
    self.progOutline = progOutline
    self.progCareer = progCareer
    self.progCategory = progCategory

class ipTracker(db.Model):
    __tablename__ = "ipTracker"

    id = db.Column(db.Integer, primary_key=True)
    userIPAddr = db.Column(db.String(128), nullable=False)
    userDeviceName = db.Column(db.String(128), nullable=False)
    userBrowserType = db.Column(db.String(128), nullable=False)
    userPlatform = db.Column(db.String(128), nullable=False)
    userBrowserVersion = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{self.userDeviceName}'

@app.route('/')
def index():

    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    device_name = socket.gethostbyaddr(ip_addr)[0]
    user_agent_string = user_agent_parser.Parse(request.headers.get('User-Agent'))
    browser_type = user_agent_string['user_agent']['family']
    browser_version = user_agent_string['user_agent']['major']
    platform = user_agent_string['os']['family']
    print(user_agent_string, ip_addr, device_name, browser_type, browser_version, platform)

    newIP = ipTracker(userIPAddr=ip_addr, userDeviceName=device_name, userBrowserType=browser_type, userBrowserVersion=browser_version, userPlatform=platform)
    db.session.add(newIP)
    db.session.commit()

    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userID = request.form.get('userID')
        password = request.form.get('password')

        if(userID == 'admin' and password == 'admin'):
            return redirect(url_for('admin', page_num=1))    
        else:
            pass
    else:
        return render_template("login.html")

@app.route('/adminEnquiry/<int:page_num>', methods=['GET', 'POST'])
def adminEnquiry(page_num):
    allEnquiry = EnquiryRequest.query.filter_by(status=True).paginate(per_page = 2, page = page_num, error_out = True)
    return render_template('admin-enquiry.html', allEnquiry=allEnquiry)

@app.route('/admin/<int:page_num>', methods=['GET', 'POST'])
def admin(page_num):
    userIP = ipTracker.query.paginate(per_page = 10, page = page_num, error_out = True)

    return render_template('admin.html', userIP = userIP)

@app.route('/enquiryChatAdmin')
def enquiryChatAdmin():
    request_id = request.args.get('chatId')
    if not request_id:
        isSessionExist = False
    else:
        isSessionExist = EnquiryRequest.query.filter_by(chatId=request_id).first()
    
    if isSessionExist:
        chatRecords = ChatMessage.query.filter_by(requestId=request_id).order_by(ChatMessage.date.asc(), ChatMessage.time.asc()).all()
    return render_template('enquiryChat-admin.html', request_id=request_id, isSessionExist=isSessionExist, chatRecords=chatRecords)

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

@app.route('/compareProg')
def compareProg():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    allProg = Programme.query.filter((Programme.progCategory == 'Degree') | (Programme.progCategory == 'Diploma')).all()

    if id2 is None:
        selectedProg = Programme.query.filter_by(progId = id1).first()
        progList= Programme.query.filter_by(progCategory = selectedProg.progCategory).all()
        compareProg = Programme.query.filter_by(progId = id2).first()
        abc = Programme.query.filter_by(progCategory = selectedProg.progCategory).first()
        id2 = abc.progId
    else:
        selectedProg = Programme.query.filter_by(progId = id1).first()
        progList= Programme.query.filter_by(progCategory = selectedProg.progCategory).all()
        compareProg = Programme.query.filter_by(progId = id2).first()
    
    return render_template("compareProg.html",allProg = allProg, prog = selectedProg, progList=progList , compareProg = compareProg)

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
    acaList = Academician.query.all()
    return render_template("testimonials.html", acaList = acaList)

@app.route('/testimonial1')
def testimonial1():
    id= request.args.get('id')
    aca = Academician.query.filter_by(acaId = id).first()
    return render_template("testimonial1.html",aca=aca)

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

@app.route('/searchProgramme', methods=["GET", "POST"])
def searchProgramme():
    programmeName = request.form["programme"]
    searchProgramme = Programme.query.filter(Programme.progName.contains(programmeName))
    results = Programme.query.filter(Programme.progName.contains(programmeName)).count()
    return render_template("searchProgramme.html", programmeName = programmeName, searchProgramme = searchProgramme, results = results)
    return 

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

subject_abbreviation = {
    "BAHASA MELAYU" : "BM" ,
    "BAHASA INGGERIS" : "BI",
    "PENDIDIKAN MORAL" : "PM",
    "SEJARAH" : "SEJ",
    "MATHEMATICS" : "MM",
    "ADDITIONAL MATHEMATICS" : "MT",
    "PHYSICS" : "FZ",
    "CHEMISTRY" : "KM",
    "BIOLOGY" : "BO",
    "BAHASA CINA" : "BC",
    "PRINSIP PERAKAUNAN" : "PP",
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
            subject_grade_dict[subject_abbreviation[subject]] = grade_dict[grade]
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
   
@app.route('/liveSupport')
def liveSupport():
    return render_template('liveSupport.html')

@app.route("/process_request", methods=['POST'])
def process_request():
    title = request.form['inputTitle']
    email = request.form['inputEmail']
    name = request.form['inputName']
    details = request.form['inputRequest']

    # Create a new EnquiryRequest object
    chatId=str(uuid.uuid4())
    new_request = EnquiryRequest(chatId=chatId, chatTitle=title, chatDetails=details, userName=name, userEmail=email, status=True)
    currentDateTime = datetime.now()
    current_date = currentDateTime.strftime("%d-%m-%Y")  # Format as desired (e.g., YYYY-MM-DD)
    current_time = currentDateTime.strftime("%I:%M%p")  # Format as desired (e.g., 10:50AM)

    new_msg = ChatMessage(time=current_time, date=current_date, content=details, sender=name, requestId=chatId)
      
    db.session.add(new_request)
    db.session.add(new_msg)
    db.session.commit()    
    status = True
    msg = Message('Hello from TARUMT Enquiry Portal', sender='hardcorestore888@gmail.com', recipients=[email])
    msg.body = f"Hello,\n\nHere is the link to the chat room: {url_for('enquiryChat', chatId=chatId, _external=True)}\n\nBest regards,\nYour Website Team"
    mail.send(msg)
    return render_template('liveSupport.html', status=status, chatId=chatId)

@app.route('/enquiryChat')
def enquiryChat():
    # Get the requestId from the query string
    request_id = request.args.get('chatId')
    if not request_id:
        isSessionExist = False
    else:
        isSessionExist = EnquiryRequest.query.filter_by(chatId=request_id).first()
    
    if isSessionExist:
        chatRecords = ChatMessage.query.filter_by(requestId=request_id).order_by(ChatMessage.date.asc(), ChatMessage.time.asc()).all()

    return render_template('enquiryChat.html', request_id=request_id, isSessionExist=isSessionExist, chatRecords=chatRecords)


connected_clients = {}
@socketio.on('connect')
def handle_connect():
    print("One client connected")


@socketio.on('addChatId')
def addChatId(data):
    chat_id = data.get('chatId')
    # Store the client's socket connection using the chat ID
    connected_clients[chat_id] = request.sid  # Store the socket ID associated with the chat ID
    print(f"{connected_clients}")

@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    #Update database
    currentDateTime = datetime.now()
    current_date = currentDateTime.strftime("%d-%m-%Y")  # Format as desired (e.g., YYYY-MM-DD)
    current_time = currentDateTime.strftime("%I:%M%p")  # Format as desired (e.g., 10:50AM)

    new_msg = ChatMessage(time=current_time, date=current_date, content=message['content'], sender=message['sender'], requestId=message['requestId'])
    db.session.add(new_msg)
    db.session.commit()    

    message['time'] = current_time
    message['date'] = current_date

    if connected_clients.get(message['requestId']):
        socketio.emit('message', message, room=connected_clients[message['requestId']])

    if connected_clients.get("admin-" + message['requestId']):
        socketio.emit('message', message, room=(connected_clients["admin-" + message['requestId']]))

@app.route('/removeChatSession', methods=['POST'])
def removeChatSession():
    print("test1111111111111111111111111")
    chatId = request.form['chatId']
    EnquiryRequest.query.filter_by(chatId=chatId).update({'status': False})
    db.session.commit()
    response_data = {"message": "Data received successfully!"}
    return jsonify(response_data)

if __name__ == "__name__":
    socketio.run(app, debug=True)
    #app.run(debug=True)


