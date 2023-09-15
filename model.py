from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    awardTitle = db.Column(db.String(300), nullable=False, unique=True)
    awardDate = db.Column(db.Date, nullable=False)
    awardPhoto = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'Item {self.awardTitle}'
    
class Event(db.Model):
    __tablename__ = "Event"

    eventId = db.Column(db.Integer(), primary_key=True)
    eventTitle = db.Column(db.String(300), nullable=False, unique=True)
    eventDate = db.Column(db.Date, nullable=False)
    eventPhoto = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'Item {self.eventTitle}'