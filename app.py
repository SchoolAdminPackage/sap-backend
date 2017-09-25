from flask import Flask, request, jsonify
from integrations.sap import SapIntegration

si = SapIntegration()

from integrations.gclassroom import initialize_integration

initialize_integration(si)

from database import Student, Teacher, Course, CourseMembership, Grade, AttendanceEvent, Period, Day, Assignment, db, PeriodToDay

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

db.init_app(app)

with app.app_context():
    db.create_all()

    db.session.add(Student(firstname="Liam", lastname="Schumm", email="lschumm@sap.edu"))
    db.session.add(Teacher(firstname="Anton", lastname="Outkine", email="aoutkine@sap.edu"))
    
    db.session.commit()

import base64

def encode(key, string):
    encoded_chars = []
    for i in xrange(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)

@app.route('/login', methods=['POST'])
def login():
    student = Student.query.filter_by(email=request.json.get('email')).first()
    teacher = Teacher.query.filter_by(email=request.json.get('email')).first()
    
    if student != None:
        return jsonify({'AccountType': 'Student'})
    
    elif teacher != None:
        return jsonify({'AccountType': 'Teacher'})
        
    else:
        return jsonify({'error': 'Invalid credentials.'})
    

@app.route('/create/student', methods=['POST'])
def create_student():
    student = Student(firstname=request.json.get('firstname'), lastname=request.json.get('lastname'), email=request.json.get('email'))
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'id': student.id,
                    'firstname': request.json.get('firstname'),
                    'lastname': request.json.get('lastname'),
                    'email': request.json.get('email'),
                    'status': 'Success'})
                    
@app.route('/create/courseMembership', methods=['POST'])
def create_courseMembership():
    mem = CourseMembership(student=Student.query.filter_by(id=int(request.json.get('id'))).first(),
                           course=Course.query.filter_by(title=request.json.get('course')).first())
    db.session.add(mem)
    db.session.commit()
    
    return jsonify({'id': int(request.json.get('id')),
                    'course': request.json.get('course')})

    
@app.route('/query/allStudents', methods=['POST'])
def all_students():
    return jsonify([{'firstname': x.firstname, 'lastname': x.lastname, 'email': x.email} for x in Student.query.all()])

@app.route('/query/allCoursesForTeacher', methods=['POST'])
def all_students_for_teacher():
    teacher = Teacher.query.filter_by(email=request.json.get('teacher_id')).first()
    return jsonify([{'title': course.title,
                     'teacher': course.teacher.email,
                     'period': course.period,
                     'students': [x.id for x in CourseMembership.query.filter_by(course=course).all()]} for course in Course.query.filter_by(teacher=teacher).all()])
                 

@app.route('/EMAILTOINT', methods=['POST'])
def EMAILTOINT():
    student = Student.query.filter_by(email=request.json.get('email')).first()
    return jsonify(student.id)

@app.route('/query/allClassAverages', methods=['POST'])
def query_grade():
    grades = Grade.query.filter(student=student).all()

    totals = {}

    for grade in grades:
        if grade.course.title in totals:
            totals[grade.course.title][0] += grade.pointsEarned
            totals[grade.course.title][0] += grade.pointsTotal
        else:
            totals[grade.course.title] = grade.pointsEarned
            totals[grade.course.title] = grade.pointsTotal

    for total in totals:
        totals[total] = totals[total][0] / totals[total][1]

    return jsonify(totals)

@app.route('/query/allGrades', methods=['POST'])
def all_grades():
    student = Student.query.filter_by(email=request.json.get('id')).first()
    
    return jsonify([{'title': x.course.title,
                     'pointsEarned': x.pointsEarned,
                     'pointsTotal': x.pointsTotal}
                    for x in Grade.query.filter_by(student=student)])
                    
@app.route('/query/allCourses', methods=['POST'])
def all_courses():
    student = Student.query.filter_by(id=int(request.json.get('id'))).first()
    
    return jsonify([{'title': x.title,
                     'teacher': x.teacher.first_name}
                     for x in CourseMembership.query.filter_by(student=student)])
    
@app.route('/create/teacher', methods=['POST'])
def create_teacher():
    teacher = Teacher(firstname=request.json.get('firstname'), lastname=request.json.get('lastname'), email=request.json.get('email'))
    db.session.add(teacher)
    db.session.commit()
    
    return jsonify({'id': teacher.id,
                    'firstname': request.json.get('firstname'),
                    'lastname': request.json.get('lastname'),
                    'email': request.json.get('email'),
                    'status': 'Success'})
    
@app.route('/create/course', methods=['POST'])
def create_course():
    si.issue('global.createClass', request.json.get('title'))
    teacher = Teacher.query.filter_by(email=request.json.get('teacher')).first()
    period = Period.query.filter_by(name=request.json.get('name')).first()
    
    student = Course(title=request.json.get('title'), teacher=teacher, period=period)
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'title': request.json.get('title'),
                    'teacher': request.json.get('teacher'),
                    'status': 'Success'})

@app.route('/query/inCourse', methods=['POST'])
def query_incourse():
    student = Student.query.filter_by(id=int(request.json.get('id'))).first()
    course = Course.query.filter_by(title=request.json.get('course')).first()

    if CourseMembership.query.filter_by(student=student, course=course).first() != None:
        return jsonify({'in_course': True,
                        'status': 'Success'})

    return jsonify({'in_course': False,
                    'status': 'Success'})

    
@app.route('/query/allInCourse', methods=['POST'])
def query_allincourse():

    students = []
    course = Course.query.filter_by(title=request.json.get('course')).first()

    for cm in CourseMembership.query.filter_by(course=course).all():
        students.append(cm.student)
        
    return jsonify([{'id': student.id,
                     'firstname': student.firstname,
                     'lastname': student.lastname,
                     'email': student.email} for student in students])
            


# @app.route('/create/coursemembership', methods=['POST'])
# def create_coursemembership():
#     course = Course.query.filter_by(title=request.json.get('course_title')).first()
#     student = Student.query.filter_by(username=request.json.get('username')).first()
#
#     cm = CourseMembership(course=course, student=student)
#
#     db.session.add(cm)
#     db.session.commit()

@app.route('/create/grade', methods=['POST'])
def create_grade():
    course = Course.query.filter_by(title=request.json.get('course_title')).first()
    student = Student.query.filter_by(id=int(request.json.get('id'))).first()
    
    grade = Grade(course=course, student=student, pointsEarned=float(request.json.get('pointsEarned')), pointsTotal=float(request.json.get('pointsTotal')))

    db.session.add(grade)
    db.session.commit()
    
    return jsonify({'course_title': request.json.get('course_title'),
                    'pointsEarned': int(request.json.get('pointsEarned')),
                    'pointsTotal': int(request.json.get('pointsTotal'))})


@app.route('/create/period', methods=['POST'])
def create_period():
    period = Period(name=request.json.get('name'))
    db.session.add(period)
    db.session.commit()

    return jsonify({'id': period.id,
                    'name': request.json.get('name')})


@app.route('/create/day', methods=['POST'])
def create_day():
    day = Day(date=request.json.get('date'))
 
#@app.route('/create/period'

# @app.route('/create/grade')
# def create_grade():
#     grade = grade(firstname=request.json.get('firstname'), lastname=request.json.get('lastname'), email=request.json.get('email'))
#     db.session.add(grade)
#     db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
