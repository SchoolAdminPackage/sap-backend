from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Student(db.Model):
    
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)

    
class Teacher(db.Model):
    
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)    

    
class Course(db.Model):
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String)
    period = db.Column(db.String)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', foreign_keys=[teacher_id])
    

class CourseMembership(db.Model):
    
    __tablename__ = 'coursememberships'
    
    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', foreign_keys=[student_id])
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', foreign_keys=[course_id])


class Grade(db.Model):
    
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', foreign_keys=[student_id])
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', foreign_keys=[course_id])
    
    pointsEarned = db.Column(db.Integer)
    pointsTotal = db.Column(db.Integer)