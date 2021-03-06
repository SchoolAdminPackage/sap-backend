import random, math, copy, csv

#preparsed info I need from db- student preferences, number of periods
#Student has preferences which is a list of tuples of Courses, and a uid
class Student:
	def __init__(self, prefs, uid):
		self.uid = uid
		self.preferences = prefs
	#Student has a .createScheduled(courses) method that returns a ProgrammedStudent with given courses and a schedule with each period to a none
	def createScheduled(self, courses):
		ss = ScheduledStudent(self.preferences, self.uid, courses, 8)
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
	#print(lc)
	#print(lc[0].period)
	#print(lc[0].uidInstance)
	#print(lc[0].students)
	#print(lc[0].uidType)
	for c in lc:
		if c == None:
			return True
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
	#each type of course
	for course in keyList:
		#every student in the course
		for student in requestsPerCourse[course]:
			switch = 1
			#if the class already has instances, see if the user can be placed in them instead of creating a new one
			if len(course.instances) > 0:
				for filledcourse in course.instances:
					if student.schedule[filledcourse.period] == None and len(filledcourse.students) < maxClassSize:
						#print("case 1")
						student.schedule[filledcourse.period] = filledcourse
						filledcourse.students.append(student)
						uidInstance += 1
						switch = 0
						break
			elif switch == 1:
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
	return new_students, filledCourses

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
		x = macroFitness(parent[1], parent[0], w1, w2)
		if x > max:
			max = x
			key = parent
	return (parent, x)

def geneticAlgorithm(students, maxClassSize, w1, w2):
	parent_student = []
	parent_classes = []
	#generates the parents for students and classes
	for i in range(30):
		p = makeParent(students, maxClassSize)
		parent_student.append(p[0])
		parent_classes.append(p[1])

	for i in range(30):
		parent_fitness = {}
		numParents = len(parent_student)
		numReproduce = numParents // 2
		#evaluates fitness for each parent tuple
		for i in range(len(parent_student)):
			parent_fitness[i] = macroFitness(parent_student[i], parent_classes[i], w1, w2)
		#print(parent_fitness)
		reproducers = list(range(numReproduce))
		for i in range(numReproduce, numParents):
			max = -1
			temp = -1
			for j in range(len(reproducers)):
				if parent_fitness[reproducers[j]] > max:
					max = parent_fitness[reproducers[j]]
					temp = j
			if parent_fitness[i] < max:
				reproducers[temp] = i
		#print(reproducers)
		nextGen = []
		random.shuffle(reproducers)
		for i in range(len(reproducers) // 2):
			mutation = mutate(parent_student[reproducers[2 * i]], parent_student[reproducers[2 * i + 1]])
			nextGen.append(mutation[0])
			nextGen.append(mutation[1])
		for index in reproducers:
			nextGen.append(parent_student[index])
		parent_student = []
		parent_student = copy.deepcopy(nextGen)
		parent_classes = []
		for students in parent_student:
			rpc = requestsPerCourse(students)
			courses = fillCourses(students, maxClassSize, rpc)
			filledCourses = getFilledCourses(courses)
			parent_classes.append(filledCourses)
		#print(parent_student)
		#print()
		#print(parent_classes)
	return parent_student, parent_classes

studentsTestData = []
def randomCoursePrefs(num, min, max):
	ans = []
	for i in range(num):
		ans.append((Course(random.randrange(min, max)), Course(random.randrange(min, max))))
	return ans
for i in range(200): 
	studentsTestData.append(Student(randomCoursePrefs(8, 1, 40), i))
#schedule = geneticAlgorithm(studentsTestData, 20, 1, 10)
#print(schedule[0])
#print(schedule[1])

#file should be in format (to input multiple for the same student keep id the same at the top):
#id ...
#main choice (course id)...
#second choice (course id)...
def parse(fi):
	f = open(fi, "r")
	with f:
		reader = csv.reader(f)
		i = 0
		ids = []
		mainpref = []
		backpref = []
		for row in reader:
			if i == 0:
				for e in row:
					ids.append(int(e))
			if i == 1:
				for e in row:
					mainpref.append(Course(int(e)))
			if i == 2:
				for e in row:
					backpref.append(Course(int(e)))
			i += 1
	studentPreferences = []
	i = 0
	ci = -1
	while i < len(ids):
		cur = ids[i]
		ci += 1
		studentPreferences.append([])
		while i < len(mainpref) and ids[i] == cur:
			studentPreferences[ci].append((mainpref[i], backpref[i]))
			i += 1
	ids = list(set(ids))
	return studentPreferences, ids


#The latter two data points can be made up if need be... student preferences should be a list of 
#list of tuples.(Each Student has their list of main choice/alts in the form of a tuple) uids 
#should be a list of the unique identifiers of the students in the same order as student preference
#you can change this a bit so long as you can get both
def createschedule(studentPreferences, uids, maxClassSize):
	students = []
	numberPeriods = len(studentPreferences[0])
	for i in range(len(studentPreferences)):
		students.append(Student(studentPreferences[i], uids[i]))
	s, c = geneticAlgorithm(students, maxClassSize, 1, 10)
	#s = list of ScheduledStudent class that contains a schedule(map: period -> course), and a uid
	#c = the list of Course instances, with period, uid, and students enrolled in it
	schedules = []
	uids = []
	for student in s[0]:
		schedules.append(student.schedule)
		uids.append(str(student.uid))
	courseInstances = c
	return schedules, uids, courseInstances

def output(f1, f2, schedules, uids, courseInstances):

	with open(f1, 'w') as csvfile:
		sf = csv.writer(csvfile)
		sf.writerow(uids)
		for i in range(len(schedules[0])):
			row = []
			for schedule in schedules:
				row.append(str(schedule[i].uidInstance))
			sf.writerow(row)
	with open(f2, 'w') as csvfile2:
		cf = csv.writer(csvfile2)
		cids = []
		periods = []
		for c in courseInstances[0]:
			cids.append(str(c.uidInstance))
			periods.append(str(c.period))
		cf.writerow(cids)
		cf.writerow(periods)

def readtowrite(f, of1, of2):
	parsed = parse(f)
	schedule = createschedule(parsed[0], parsed[1], 30)
	output(of1, of2, schedule[0], schedule[1], schedule[2])

#def makeRandom(fi):
#	with open(fi, 'w') as csvfile:
#		fw = csv.writer(csvfile)
#		ids = []
#		for i in range(200):
#			for j in range(8):
#				ids.append(str(i))
#		fw.writerow(ids)
#		row = []
#		for i in range(800):
#			row.append(str(random.randrange(1,40)))
#			row.append(str(random.randrange(1,40)))
#		fw.writerow(row)
#		row = []
#		for i in range(800):
#			row.append(str(random.randrange(1,40)))
#			row.append(str(random.randrange(1,40)))
#		fw.writerow(row)
#makeRandom('test.csv')
readtowrite('test.csv', 'students.csv', 'courses.csv')