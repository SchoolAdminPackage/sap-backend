from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Day(db.Model):

    __tablename__ = 'days'

    id = db.Column(db.Integer, primary_key=True)

    # iso 8601
    date = db.Column(db.String)


class PeriodToDay(db.Model):

    __tablename__ = 'periodtodays'

    id = db.Column(db.Integer, primary_key=True)

    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))
    period = db.relationship('Period', foreign_keys=[period_id])

    day_id = db.Column(db.Integer, db.ForeignKey('days.id'))
    day = db.relationship('Day', foreign_keys=[day_id])
    
    
class Period(db.Model):

    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


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

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    assignment = db.relationship('Assignment', foreign_keys=[assignment_id])


class Assignment(db.Model):

    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', foreign_keys=[course_id])

    # iso 8601 format
    dueDate = db.Column(db.String)

