import requests
import json


print("--------------------------- WELCOME TO SARAL ----------------------------")

def getUrl(url):
	link = requests.get(url)
	dictionary = json.loads(link.text)
	return dictionary
#Here i've made a function to call API and get data

dictionary = getUrl("http://saral.navgurukul.org/api/courses")   #Here i'm calling saral URL
with open ("simple_courses.json","w") as f:
	json.dump(dictionary,f)
#Here i'm dumpping saral data in a file named simple_courses.json

#Here i'm accessing a list named availableCourses inside the dictionary
courses = dictionary["availableCourses"]

# I've made again a function named list_of_course for accessing main course list.
def list_of_course():
	courses = dictionary["availableCourses"]
	counter = 0
	while counter < len(courses):
		course_name = courses[counter]["name"]
		print (counter,course_name)
		counter=counter+1
list_of_course()

def courseid_list():
	courses_id_list =[]
	courses_list = []
	counter = 0
	while counter < len(courses):
		course_id = courses[counter]["id"]
		course_name = courses[counter]["name"]
		courses_id_list.append(course_id)
		courses_list.append(course_name)
		counter=counter+1
#Here i'm appending course id in courses_id_list and course name in courses_list

#Here i'm taking user input for getting selected course by user
	courseId = int(input("Enter course id: "))  
	print ("Your selected course name is", courses_list[courseId], "and couser ID is", courses_id_list[courseId])

#Here i;m calling again getUrl function for to call API for getting parants and their child 
	callApi = getUrl("http://saral.navgurukul.org/api/courses"+"/"+courses_id_list[courseId]+"/"+"exercises")
	exercise = callApi["data"]
	parent_exercise_name = []
	childExercises = []
	i=0
	while i < len(exercise):
		parent_exercise_name.append(exercise[i]['name'])
		childExercises.append(exercise[i]['childExercises'])	
		print (i,exercise[i]['name'])
		second_parant = exercise[i]['childExercises']
		j=1
		while j < len(second_parant):
			if "parent_exercise_id" in second_parant[j]:
				print(5*' '+str(j),second_parant[j]['name'])
			j=j+1
		i=i+1

# In funtion up_down either will be go back to main course if user will enter up or if user will enter no. then will go inside that course
	def up_down():
		exerciseUpdown = input("Enter 'up' or exercise no.: ")  
		if exerciseUpdown == "up":      
			(list_of_course()) 
			(courseid_list())
		elif type(exerciseUpdown) == str:
			exerciseNo = int(exerciseUpdown)    #We can't access a list with string so i'm converting here a string in to integer
			print(0,exercise[exerciseNo]['name'])
			child_list=[]
			child_slug = []
			i=1
			for child in exercise[exerciseNo]['childExercises']:
				print(5*' ',i,child['name'])
				child_list.append(child['name'])
				child_slug.append(child['slug'])
				i=i+1
	#Here we are taking user input of exercise no. in user variable for getting it's correspondence content	
		user = int(input("Enter exercise no. for getting correspondence content: "))  #Here was user1
		exerciseId = exerciseNo-1    #Here was user3=user-1
		get_content = getUrl("http://saral.navgurukul.org/api/courses/"+courses_id_list[exerciseId]+"/exercise/getBySlug?slug="+child_slug[exerciseId])
		print("\n")
		print (get_content['content'])

	#Here if user'll enter p user'll back to previouse content and if user'll enter n user'll go to next content
	# If page will end you will get page not found
		j=0
		while j < len(child_list)-1:
			nextPrevious = input("Enter 'n' for next or 'p' for previous: ")   #Here was user1 
			if nextPrevious == "n":
				i=0
				while i<len(child_list):
					exerciseId=exerciseId+1
					get_contents = getUrl("http://saral.navgurukul.org/api/courses/"+courses_id_list[exerciseId]+"/exercise/getBySlug?slug="+child_slug[exerciseId])
					print(get_contents['content'])
					break
					i=i+1
					print("\n")
			elif nextPrevious == "p":
				i=0
				while i<len(child_list):
					exerciseId=exerciseId-1
					get_contents = getUrl("http://saral.navgurukul.org/api/courses/"+courses_id_list[exerciseId]+"/exercise/getBySlug?slug="+child_slug[exerciseId])
					print(get_contents['content'])
					break
					i=i+1
			j=j+1
		else:
			print("Page not found")
	
	up_down()
	
courseid_list()
