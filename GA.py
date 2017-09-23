import random

#Student has preferences which is a list of tuples of Courses, and a uid
class Student(object):
	def __init__(self, prefs, uid):
		uid = uid
		preferences = prefs
	#Student has a .createScheduled(courses) method that returns a ProgrammedStudent with given courses and a schedule with each period to a null
	def createScheduled(courses):
		return ScheduledStudent(prefs, uid, courses, 4)
#ScheduledStudent is a subclass of Student that has a list of Courses and a schedule
class ScheduledStudent(Student):
	def __init__(self, prefs, uid, courses, numPeriods):
		super().__init__(prefs, uid)
		courses = courses
		#Schedule is an dictionary of integers to FilledCourses
		schedule = {}
		for i in range(numPeriods):
			schedule[i] = null

#Course has a uidType and instances(starts as [])
class Course():
	def __init__(self, uid):
		uidType = uid
		instances = []
	#has a .createFilled(uidInstance, period) that  creates a FilledCourse, adds it to instances, instantiates an empty list of students
	def createFilled(uidInstance, period):
		fc = FilledCourse(uidType, uidInstance, period)
		instances.append(fc)
		return fc
#FilledCourse is a subclass of CourseInstance that has a list of students registered for the class, a period(unique integer is all that matters), and a uidInstance
class FilledCourse(Course):
	def __init__(self, uidType, uid, per):
		super().__init__(uidType)
		period = per
		uidInstance = uid
		students = []

#parse function (input) -> list of [students]
#def parseData(data):
	#return list of students

#determines preference error for one student
#returns number of first choices that were selected
def microFitnessw1(student):
	sum = 0
	for pref in student.preferences:
		if pref[1] in student.schedule.itervalues():
			sum += 1
	return sum

#determines preference error for whole system
def macroFitnessw1(scheduledStudents):
	sum = 0
	for student in scheduledStudents:
		sum += microFitnessw1(student)
	return sum

#determines class size error for whole system
def macroFitnessw2(courses):
	sum = 0
	for course in courses:
		for filledCourse in course.instances:
			sum += 1
	return sum

#determines fitness of whole system (should be minimized)
def macroFitness(scheduledStudents, courses, maxClassSize, w1, w2):
	return w1 * macroFitnessw1(scheduledStudents) + w2 * macroFitnessw2(courses, maxClassSize)

#generates all students courses for one parent
def makeStudentCourses(students):
	newStudents = []
	for student in students:
		courses = []
		for prefPair in student.preferences:
			courses.append(random.choice(prefPair))
		newStudents.append(student.createScheduled(courses))
	return newStudents

#gets which students are getting each class
def requestsPerCourse(students, maxClassSize):
	#dict to show how many people selected each course
	requestsPerCourse = {}
	#to make sure the instance id for each course remains unique
	courseInstaceIdCounter = 0
	courses = []
	for student in students:
		for course in courses:
			if preference in requestsPerCourse.iterkeys():
				requestsPerCourse[course].append(student)
			else:
				requestsPerCourse[course] = [student]
	return requestsPerCourse

def firstAvailiblePeriod(student):
	for period in student.schedule.iterkeys():
		if student.schedule[period] == null:
			return period
	console.log("no available periods")
	return -1

#generates randomly filled courses for one parent 
def fillCourses(students, maxClassSize, requestsPerCourse):
	#counts uid to avoid duplicates
	uidInstance = 0
	switchVarCuzImBadAndNeedACrutch = 1
	keyList = random.shuffle(requestsPerCourse.iterkeys())
	for course in keyList:
		for student in requestsPerCourse[course]:
			for filledcourse in course.instances:
				if student.schedule[filledcourse.period] == null and len(filledcourse.students) < maxClassSize:
					student.schedule[filledcourse.period] = FilledCourse
					filledcourse.students.append(student)
					switchVarCuzImBadAndNeedACrutch = 0
					break
			if (switchVarCuzImBadAndNeedACrutch):
				newFilled = course.createFilled(uidInstance, firstAvailiblePeriod(student))
				student.schedule[firstAvailiblePeriod(student)] = newFilled
				newFilled.students.add(student)
				uidInstance += 1
	return keyList

def getFilledCourses(courses):
	filledCourses = []
	for course in courses:
		filledCourses.extend(course.instances)
	return filledCourses

#gets a list of scheduledStudents and the filledCourses in the "parent" world
def makeParent(students, maxClassSize):
	new_students = makeStudentCourses(students)
	studentsPerCourse = requestsPerCourse(new_students, maxClassSize)
	courses = fillCourses(new_students, maxClassSize, studentsPerCourse)
	filledCourses = getFilledCourses(courses)
	return filledCourses, new_students

#mutate a list of scheduledStudents
def mutate(l1, l2):
	l3 = []
	mutation = []
	for i in range(len(l1)):
		mutation.append(random.randrange(0,2))
		for j in range(len(l2)):
			if l1[i].uid == l2[j].uid:
				l3.append(l2[j])
	l4 = []
	l5 = []
	for i in range(len(l3)):
		if mutation[i] == 0:
			l4.append(l1[i])
			l5.append(l3[i])
		else:
			l4.append(l3[i])
			l5.append(l1[i])
	return l4, l5

#returns the least fit in the list
def getHighestFitness(parents, w1, w2):
	max = -1
	for parent in parents:
		x = macroFitness(parent[1], parent[0], maxClassSize, w1, w2)
		if x > max:
			max = x
			key = parent
	return (parent, x)

def geneticAlgorithm(students, maxClassSize, w1, w2):
	parents = []
	for i in range(64):
		parents.append(makeParent(students, maxClassSize))
	for i in range(7):
		parentFitness = {}
		numSurvivors = math.ceil(parents / 2)
		survivors = []
		highestFitness = (null, -1)
		for parent in parents:
			parentFitness[parent] = macroFitness(parent[1], parent[0], maxClassSize, w1, w2)
			if len(survivors) < numSurvivors:
				survivors.append(parent)
				if parentFitness[parent] > highestFitness[1]:
					highestFitness = (parent, parentFitness[parent])
			elif parentFitness[parentFitness] < highestFitness[1]:
				survivors.append(parent)
				survivors.remove(highestFitness[0])
				highestFitness = getHighestFitness(survivors) 
		parents = []
		for i in range(survivors // 2):
			childrenStudents = mutate(survivors[2 * i][1], survivors[2 * i + 1][1])
			studetnsPerCourse = requestsPerCourse(childrenStudents, maxClassSize)
			courses = fillCourses(childrenStudents, maxClassSize, studentsPerCourse)
			filledCourses = getFilledCourses(courses)
			parents.append((filledCourses, childrenStudents))
		print(parentFitness)
	return parents
studentsTestData = []
coursesTestData = []
for i in range(4):
	coursesTestData.append((Course(2 * i), Course(2 * i + 1)))
for i in range(100):
	studentsTestData.append(Student(coursesTestData, i))
geneticAlgorithm(studentsTestData, 20, 1, 4)