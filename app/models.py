from app import db


##############################################################
# MODELS #####################################################
class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    date_joined = db.Column(db.DateTime())
    is_admin = db.Column(db.Boolean)
    courses = db.relationship('Course', backref='user', lazy='dynamic')


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))