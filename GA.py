import random, math

#Student has preferences which is a list of tuples of Courses, and a uid
class Student:
	def __init__(self, prefs, uid):
		self.uid = uid
		self.preferences = prefs
	#Student has a .createScheduled(courses) method that returns a ProgrammedStudent with given courses and a schedule with each period to a none
	def createScheduled(self, courses):
		ss = ScheduledStudent(self.preferences, self.uid, courses, 4)
		return ss
#ScheduledStudent is a subclass of Student that has a list of Courses and a schedule
class ScheduledStudent(Student):
	def __init__(self, prefs, uid, courses, numPeriods):
		self.uid = uid
		self.preferences = prefs
		self.courses = courses
		#Schedule is an dictionary of integers to FilledCourses
		self.schedule = {}
		for i in range(numPeriods):
			self.schedule[i] = None

#Course has a uidType and instances(starts as [])
class Course:
	def __init__(self, uid):
		self.uidType = uid
		self.instances = []
	#has a .createFilled(uidInstance, period) that  creates a FilledCourse, adds it to instances, instantiates an empty list of students
	def createFilled(self, uidInstance, period):
		fc = FilledCourse(self.uidType, uidInstance, period)
		self.instances.append(fc)
		return fc
#FilledCourse is a subclass of CourseInstance that has a list of students registered for the class, a period(unique integer is all that matters), and a uidInstance
class FilledCourse(Course):
	def __init__(self, uidt, uid, per):
		self.uidType = uidt
		self.period = per
		self.uidInstance = uid
		self.students = []

#parse function (input) -> list of [students]
#def parseData(data):
	#return list of students

def typeIn(int, lc):
	print(lc)
	print(lc[0].period)
	print(lc[0].uidInstance)
	print(lc[0].students)
	print(lc[0].uidType)
	for c in lc:
		if int == c.uidType:
			return True
	return False
#determines preference error for one student
#returns number of first choices that were selected
def microFitnessw1(student):
	sum = 0
	#print(list(student.schedule.values()))
	for pref in student.preferences:
		if typeIn(pref[1].uidType, list(student.schedule.values())):
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
			sum += 1
	return sum

#determines fitness of whole system (should be minimized)
def macroFitness(scheduledStudents, courses, w1, w2):
	return w1 * macroFitnessw1(scheduledStudents) + w2 * macroFitnessw2(courses)

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
def requestsPerCourse(students):
	#dict to show how many people selected each course
	requestsPerCourse = {}
	#to make sure the instance id for each course remains unique
	courseInstaceIdCounter = 0
	courses = []
	for student in students:
		for course in student.courses:
			if course in list(requestsPerCourse.keys()):
				requestsPerCourse[course].append(student)
			else:
				requestsPerCourse[course] = [student]
	return requestsPerCourse

def firstAvailiblePeriod(student):
	for period in list(student.schedule.keys()):
		if student.schedule[period] == None:
			return period
	print("no available periods")
	return -1

#generates randomly filled courses for one parent 
def fillCourses(students, maxClassSize, requestsPerCourse):
	#counts uid to avoid duplicates
	uidInstance = 0
	keyList = list(requestsPerCourse.keys())
	random.shuffle(keyList)
	for course in keyList:
		for student in requestsPerCourse[course]:
			switchVarCuzImBadAndNeedACrutch = 1
			for filledcourse in course.instances:
				print(student.schedule[filledcourse.period] )
				if student.schedule[filledcourse.period] == None and len(filledcourse.students) < maxClassSize:
					#print("case 1")
					student.schedule[filledcourse.period] = course.createFilled(uidInstance, filledcourse.period)
					filledcourse.students.append(student)
					uidInstance += 1
					switchVarCuzImBadAndNeedACrutch = 0
					break
			if (switchVarCuzImBadAndNeedACrutch == 1):
				#print("case 2")
				newFilled = course.createFilled(uidInstance, firstAvailiblePeriod(student))
				student.schedule[firstAvailiblePeriod(student)] = newFilled
				newFilled.students.append(student)
				uidInstance += 1
	return list(requestsPerCourse.keys())

def getFilledCourses(courses):
	filledCourses = []
	for course in courses:
		filledCourses.extend(course.instances)
	return filledCourses

#gets a list of scheduledStudents and the filledCourses in the "parent" world
def makeParent(students, maxClassSize):
	new_students = makeStudentCourses(students)
	studentsPerCourse = requestsPerCourse(new_students)
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
	for i in range(6):
		parentFitness = []
		numSurvivors = math.ceil(len(parents) / 2)
		survivors = []
		highestFitness = (None, -1)
		for parent in parents:
			print(macroFitnessw1(parent[1]))
			print(macroFitnessw2(parent[0]))
			x = macroFitness(parent[1], parent[0], w1, w2)
			parentFitness.append(x)
			if len(survivors) < numSurvivors:
				survivors.append(parent)
				if x > highestFitness[1]:
					highestFitness = (parent, x)
			elif x < highestFitness[1]:
				survivors.append(parent)
				survivors.remove(highestFitness[0])
				highestFitness = getHighestFitness(survivors) 
		parents = []
		for i in range(len(survivors) // 2):
			childrenStudents = mutate(survivors[2 * i][1], survivors[2 * i + 1][1])
			studentsPerCourse = requestsPerCourse(childrenStudents[0])
			courses = fillCourses(childrenStudents[0], maxClassSize, studentsPerCourse)
			filledCourses = getFilledCourses(courses)
			parents.append((filledCourses, childrenStudents[0]))
			studentsPerCourse = requestsPerCourse(childrenStudents[1])
			courses = fillCourses(childrenStudents[1], maxClassSize, studentsPerCourse)
			filledCourses = getFilledCourses(courses)
			parents.append((filledCourses, childrenStudents[1]))
		print(parentFitness)
	return parents
studentsTestData = []
coursesTestData = []
for i in range(4):
	coursesTestData.append((Course(2 * i), Course(2 * i + 1)))
for i in range(100):
	studentsTestData.append(Student(coursesTestData, i))
geneticAlgorithm(studentsTestData, 20, 1, 4)