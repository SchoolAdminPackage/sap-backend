from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Day(db.Model):

    __tablename__ = 'days'

    id = db.Column(db.Integer, primary_key=True)

    # iso 8601
    date = db.Column(db.String)

    def __json__(self):
        return {'date': self.date}
    

class PeriodToDay(db.Model):

    __tablename__ = 'periodtodays'

    id = db.Column(db.Integer, primary_key=True)

    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))
    period = db.relationship('Period', foreign_keys=[period_id])

    day_id = db.Column(db.Integer, db.ForeignKey('days.id'))
    day = db.relationship('Day', foreign_keys=[day_id])

    def __json__(self):
        return {'period': period.__json__(),
                'day': day.__json()}
    
    
class Period(db.Model):

    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __json__(self):
        return {'name': self.name}


class Student(db.Model):
    
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)

    def __json__(self):
        return {'firstname': self.firstname,
                'lastname': self.lastname,
                'email': self.email}

    
class Teacher(db.Model):
    
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)    

    def __json__(self):
        return {'firstname': self.firstname,
                'lastname': self.lastname,
                'email': self.email}
    
    
class Course(db.Model):
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String)
    period = db.Column(db.String)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', foreign_keys=[teacher_id])

    def __json__(self):
        return {'title': self.title,
                'period': self.period.__json__(),
                'teacher': self.teacher.__json__()}
    

class CourseMembership(db.Model):
    
    __tablename__ = 'coursememberships'
    
    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', foreign_keys=[student_id])
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', foreign_keys=[course_id])

    def __json__(self):
        return {'student': self.student.__json__(),
                'course': self.course.__json__()}
    
    
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
    
    title = db.Column(db.String)


    def __json__(self):
        return {'student': self.student.__json__(),
                'course': self.course.__json__(),
                'pointsEarned': self.pointsEarned}
                
    

class Assignment(db.Model):

    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', foreign_keys=[course_id])

    # iso 8601 format
    dueDate = db.Column(db.String)

    def __json__(self):
        return {'name': self.name,
                'course': self.course.__json__()}
                

class AttendanceEvent(db.Model):
    
    __tablename__ = 'attendanceevents'
    
    id = db.Column(db.Integer, primary_key=True)
    
    date = db.Column(db.String)
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', foreign_keys=[student_id])
    
    tardy = db.Column(db.Boolean, default=True)
    
    def __json__(self):
            return {'date': self.date,
                    'tardy': self.tardy,
                    'student': self.student.__json__()}
