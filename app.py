from flask import Flask, request, jsonify

from database import Student, Teacher, Course, CourseMembership, Grade, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

db.init_app(app)

with app.app_context():
    db.create_all()

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
    
@app.route('/query/allStudents', methods=['POST'])
def all_students():
    return jsonify([{'firstname': x.firstname, 'lastname': x.lastname, 'email': x.email} for x in User.query().all()])
    
@app.route('/query/allGrades', methods=['POST'])
def all_grades():
    student = Student.query.filter_by(username=request.json.get('username')).first()
    
    return jsonify([{'title': x.course.title,
                     'pointsEarned': x.pointsEarned,
                     'pointsTotal': x.pointsTotal}
                    for x in Grade.query.filter_by(student=student)])
    
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
    teacher = Teacher.query.filter_by(id=int(request.json.get('teacher'))).first()
    
    student = Course(title=request.json.get('title'), teacher=teacher)
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'title': request.json.get('title'),
                    'teacher': int(request.json.get('teacher')),
                    'status': 'Success'})
    
@app.route('/create/coursemembership', methods=['POST'])
def create_coursemembership():
    course = Course.query.filter_by(title=request.json.get('course_title')).first()
    student = Student.query.filter_by(username=request.json.get('username')).first()
    
    cm = CourseMembership(course=course, student=student)

    db.session.add(cm)
    db.session.commit()

@app.route('/create/grade', methods=['POST'])
def creat_grade():
    course = Course.query.filter_by(title=request.json.get('course_title')).first()
    student = Student.query.filter_by(username=request.json.get('username')).first()
    
    grade = Grade(course=course, student=student, pointsEarned=float(request.json.get('pointsEarned')), pointsTotal=float(request.json.get('pointsTotal')))

    db.session.add(grade)
    db.session.commit()
    
# @app.route('/create/grade')
# def create_grade():
#     grade = grade(firstname=request.json.get('firstname'), lastname=request.json.get('lastname'), email=request.json.get('email'))
#     db.session.add(grade)
#     db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)