from genericpath import exists
from logging import exception
from multiprocessing import context
from pyexpat import model
import re
from django.shortcuts import render, redirect
from .models import Course, Evaluation, User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.template.defaulttags import register
from django import forms
from django.contrib import messages
from datetime import datetime, timedelta
import calendar
# from django import template
  
# register= template.Library()
#split 
@register.filter(name='split_subtasks')
def split_subtasks(value):
    """
        Returns the value turned into a list.
    """
    #chr(10) is the unicode for \n
    # another way: v = list (value.split(chr(10)))
    if value:
        
        v = list (value.split('\n'))
    else:
        v = ""
    print(v)
    return v
#Don't need this filt since python by default will split by /n

# Create your views here.
#home page
def homePage(request):
    return render(request,'index.html')



def loginPage(request):

    #if request.user.is_authenticated:
        #return redirect('homePage')
    
    if request.method == 'POST':
        
        print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        #validate
        try:
            user = User.objects.get(email = email)
        except:
            print( 'Email does not exist')
            #add flash message
        #print("hi")
        #check to see if user info mat
        user = authenticate(request,username = email, password = password)
        #send user to their dashboard page

        #check if autehications was successful
        if user is not None:
            print(user)
            login(request,user)
            return redirect('home')
        else:
            print('Email or password is incorrect')
            #add flash message  
    return render(request, 'registration/login.html')

def logoutUser(request):
    logout(request)
    return redirect ('login')


#Registeration Form 
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username','dateOfBirth','postSecondaryInstitution', 'email', 'password1', 'password2']    

    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__(*args, **kwargs) 

def registerPage (request):
    form = RegisterForm()

    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(request.POST)

        #check to see if regestration info is valid
        if form.is_valid():
            print("form was valid")
            # user = form.save(commit=False)
            # user.username = user.email
            # user.save()
            form.save()
            print("form saved")

    #field Name that will passed to the form and how it will appear
    fieldNames = {'first_name':"First Name",'last_name':"Last Name", 'username':"Forum Display Name",'dateOfBirth':"Date of Birth",'postSecondaryInstitution':"Post Secondary Institution", 'email':"Email Address", 'password1':"Password", 'password2':"Re-type Password"}
    return render(request, 'registration/register.html', {"form":form,"fieldNames":fieldNames})


def profilePage(request,pk):
    userProfile = User.objects.get(id=pk)
    context = {'profile':userProfile}
    return render(request, 'profile.html',context)

#Profile Form needed for user to be able to edit profile
class EditedProfile(forms.ModelForm):
    dateOfBirth = forms.DateField(required=True)
    postSecondaryInstitution = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'dateOfBirth','postSecondaryInstitution', 'email']    

def editProfile(request,pk):
    #userProfile = User.objects.get(id=pk)
    form = EditedProfile(request.POST, instance = request.user)
    print(request.POST)
    print("hello")
    if form.is_valid():
        print("form valid")
        form.save()
        return redirect('profile', request.user.id)
    #PSI = array of Post Secondary Institution - is at the bottom of page
    context = {'PSI' : PSI}
    #do I need a seperate form with only the particular editable fields?
    return render (request, 'edit_profile.html', context)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['owner','courseName','courseCode', 'numOfCredits','totalAssignments', 'totalMidTerms','has_FinalExam','currentGrade','finalGrade','completionProgress']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['course','date','type','subtasks','gradeWeight','grade']

def courseCreation(request):
    # 'courseName': ['Intro'], 'courseCode': ['COMP1001'], 'numOfCredits': ['4'], 'assignment[1][date]': ['2022-09-13'], 'assignment[1][gradeWeight]': ['20'], 'assignment[1][subTask][]': ['finish page', 'finish title'], 'assignment[2][date]': ['2022-09-05'], 'assignment[2][gradeWeight]': ['4'], 
    # 'assignment[2][subTask][]': ['finish tomorrow']
    print(request.POST)
    print("I was here")
    courseCreationSuccessful = False
    
    if(request.method == "POST"):
        currentGrade = 0
        evalutionGrades = []
        finalGrade = 0
        completionProgress = 0
        assignMidtermWithoutGrade = False
        returnOnErrors = False

        for i in request.POST.getlist('assignment-counter'):
            try:
                if (request.POST["assignment-"+ i +"-grade"]) == "":
                    assignMidtermWithoutGrade = True
                else:
                    evalutionGrades.append(request.POST["assignment-"+ i +"-grade"])
                    completionProgress += int(request.POST["assignment-"+ i +"-gradeWeight"])
                    finalGrade += (int(request.POST["assignment-"+ i +"-gradeWeight"])/100) * int(request.POST["assignment-"+ i +"-grade"])
                    print("assignmen")
            except:
               pass

        for j in request.POST.getlist('midterm-counter'):
            try:
                if (request.POST["midterm-"+ i +"-grade"]) == "":
                    assignMidtermWithoutGrade = True
                else:
                    evalutionGrades.append(request.POST["midterm-"+ i +"-grade"])
                    completionProgress += int(request.POST["midterm-"+ i +"-gradeWeight"])
                    finalGrade += (int(request.POST["midterm-"+ i +"-gradeWeight"])/100) * int(request.POST["midterm-"+ i +"-grade"])
                    print("midterm")
            except:
               pass

        try:

            if request.POST["finalExamGrade"] != "":
                evalutionGrades.append(request.POST["finalExamGrade"])
                completionProgress += int(request.POST["fianlExamGradeWeight"])
                finalGrade += (int(request.POST["fianlExamGradeWeight"])/100) * int(request.POST["finalExamGrade"]) 
                print("final exam")
                #set current grade as -1, since a grade for final exam means student has completed course
                currentGrade = -1
            else:
                currentGrade = sum(map(int,evalutionGrades))/len(evalutionGrades)
                finalGrade = -1   
        except Exception as e:
            currentGrade = sum(map(int,evalutionGrades))/len(evalutionGrades)
            finalGrade = -1
            print(e)
            

       
        try:

            if request.POST["finalExamGrade"] != "" and assignMidtermWithoutGrade == True:
                messages.error(request,"Must enter grades for all assignments and midterms before entering final exam grade!")
                returnOnErrors = True                
        except:
            pass


        #check if grade weight is = 100 or less than for applicable evaluation type
        totalGradeWeight = 0
        try:
            totalGradeWeight += int(request.POST["fianlExamGradeWeight"])
        except:
            pass
        try:
            for j in request.POST.getlist('midterm-counter'):
                totalGradeWeight += int(request.POST["midterm-"+ i +"-gradeWeight"])
        except:
            pass
        #why is this not in a try except as well?
        try:
            for i in request.POST.getlist('assignment-counter'):
                totalGradeWeight += int(request.POST["assignment-"+ i +"-gradeWeight"])
        except:
            pass
        
    

        #pass error message since total grade weight exceeds 100%
        if totalGradeWeight != 100:
            #flash message to create-course page
            messages.error(request, 'Total grade weight for all evaluations must equal 100 grade weight!')
            returnOnErrors = True
        if returnOnErrors:
            context = {'userData': request.POST}
            return render (request, 'create_course.html',context)


        #add course information into dictionary
        courseDict = {'courseName': request.POST['courseName'], 
            'courseCode':request.POST['courseCode'],
            'numOfCredits': request.POST['numOfCredits'],
            'currentGrade': currentGrade, 'completionProgress' : completionProgress,
            'finalGrade' : finalGrade}
        
        try:
            courseDict["totalAssignments"] = len(request.POST.getlist('assignment-counter'))
        except:
            courseDict["totalAssignments"] = 0

        try:
            courseDict["totalMidTerms"] = len(request.POST.getlist('midterm-counter'))
        except:
            courseDict["totalMidTerms"] = 0

        if "has_FinalExam" in request.POST:
            courseDict["has_FinalExam"] = True
        else:
            courseDict["has_FinalExam"] = False
        #error message if user tries submitting a course with 0 evaluations
        if courseDict["totalAssignments"] == 0 and courseDict["totalMidTerms"] == 0 and courseDict["has_FinalExam"] == False:
            messages.error(request,"Course must have an evaluation!")
            return render (request, 'create_course.html')

        courseDict["owner"] = request.user.id
        form = CourseForm(courseDict)
        
        
        print(courseDict)
        if form.is_valid():
            print("course valid")
            course = form.save()
            courseCreationSuccessful = True
        else:
            courseCreationSuccessful = False
            
        # ---------------------------------
        assignmentDict= {}
        assignmentDict['course'] = course.id

        for i in request.POST.getlist('assignment-counter'):
            assignmentDict['date'] = request.POST["assignment-"+ i +"-date"]
            assignmentDict['gradeWeight'] = request.POST["assignment-"+ i +"-gradeWeight"]
            assignmentDict['grade'] = request.POST["assignment-"+ i +"-grade"]
            print("Assignment Grade")
            print(request.POST["assignment-"+ i +"-grade"])
            try:
                assignmentDict['subtasks'] = "\n".join(request.POST.getlist("assignment-"+ i +"-subTask"))
            except:
                pass
            assignmentDict['type'] = "assignment"
            form = EvaluationForm(assignmentDict)
            print("assignment Validation")
            print(assignmentDict)
            if form.is_valid():
                print("assignment valid")
                form.save() 

        midtermDict ={}
        midtermDict['course'] = course.id
        try:
            for j in request.POST.getlist('midterm-counter'):
                midtermDict['date'] = request.POST["midterm-"+ i +"-date"]
                midtermDict['gradeWeight'] = request.POST["midterm-"+ i +"-gradeWeight"]
                midtermDict['grade'] = request.POST["midterm-"+ i +"-grade"]
                try:
                    midtermDict['subtasks'] = "\n".join(request.POST.getlist("midterm-"+ i +"-subTask"))
                except:
                    pass
                midtermDict['type'] = "midterm"
                form = EvaluationForm(midtermDict)
                print("midterm Validation")
                print(midtermDict)
                if form.is_valid():
                    print("midterm valid")
                    form.save()
        except:
            print("no midterm")

        finalExamDict = {}
        finalExamDict['course'] = course.id
        try:
            if courseDict["has_FinalExam"]:
                finalExamDict['date'] = request.POST["finalExamDate"]
                finalExamDict['gradeWeight'] = request.POST["fianlExamGradeWeight"]
                finalExamDict['grade'] = request.POST["fianlExamGrade"]
                print("Exam Grade")
                print(request.POST["fianlExamGrade"])
                try:
                    finalExamDict['subtasks'] = "\n".join(request.POST.getlist("finalExamMaterial"))
                except:
                    pass
                finalExamDict['type'] = "finalexam"
                form = EvaluationForm(finalExamDict)
                print("finalExam Validation")
                print(finalExamDict)
                if form.is_valid():
                    print("finalExam valid")
                    form.save()
        except:
            print("no final exam")
            
        if courseCreationSuccessful:
            messages.success(request,"Course added successfully!")
        else:
            messages.error(request, "Course couldn't be added...")
                
    #print(request.POST['assignment[1]'])
    #print(request.POST['assignment'])
    # there functions to dictionary in python: keys(), values() and items() -> will give keys and values
    #assignments = [k for k in request.POST.keys() if k.startswith('assignment')]
    #assignments = len(request.POST.getlist('assignment-counter'))
    #midterms = len(request.POST.getlist('midterm-counter'))
    #for()
    
    #print(assignments)
    #midterms = [k for k in request.POST.keys() if k.startswith('midterm')]
    #print(midterms)
    
    return render (request, 'create_course.html')

@register.filter
def get_evaluation_by_type(course,type):

    return course.evaluation_set.filter(type=type)

@register.filter
def checking_type(course,type):
    if course.evaluation_set.filter(type=type):
        print(course.courseCode + ":true")
        return True

    else:
        print(course.courseCode + ":false")
        return False

        

#sk is search key
def currentCourse(request, sk=""):
    if sk == "":
        courses = Course.objects.filter(owner = request.user.id)
    else:
        courses = Course.objects.filter(owner = request.user.id).filter(courseCode__contains=sk)

    context = {'courses': courses}

    return render (request, 'current_course.html',context)

def editCourse(request):
    return render(request, 'edit_course_new.html')

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def userDash(request):
    courses = Course.objects.filter(owner = request.user.id)
    context = {'courses':courses}
    return render (request, 'user_dashboard.html', context)

def importantDates(request,frq='all'):
    print(frq)
    courses = Course.objects.filter(owner = request.user.id)
    #evaluations
    evs = []
    dt = datetime.today()

    #find start of the week
    #dt.weekday() gives position of today's date's current position from Monday 
    #timedelta converts to date object so that it can be subtracted from today's date to Monday
    start = dt - timedelta(days=dt.weekday()) 

    #add 6 to get Sunday
    end = start +  timedelta(days=6) 
    #format date
    weeklyStart = start.strftime('%Y-%m-%d')
    weeklyEnd = end.strftime('%Y-%m-%d')


    # 14 days starting from the monday 
    biWeeklyStart = start
    biWeeklyEnd = start + timedelta(days=13)
    #format date
    biWeeklyStart = biWeeklyStart.strftime('%Y-%m-%d')
    biWeeklyEnd = biWeeklyEnd.strftime('%Y-%m-%d')

    #check which button was clicked and get evaluations accordiongly 
    if frq == "all":
        for c in courses:
            evs.append(c.evaluation_set.all())

    elif frq == "weekly":
        for c in courses:
            evs.append(c.evaluation_set.filter(date__range = [weeklyStart,weeklyEnd]))

    elif frq == "biweekly":
        for c in courses:
            evs.append(c.evaluation_set.filter(date__range = [biWeeklyStart,biWeeklyEnd]))

    elif frq == "monthly":
        for c in courses:
            #filter(date__year = dt.year,date__month = dt.month)) django will automatically find start and end date for that month for 
            #current year
            evs.append(c.evaluation_set.filter(date__year = dt.year,date__month = dt.month))
    
    context = {'courses': courses, 'evs': evs}
    return render(request,'important_dates.html', context)

def editTasks(request, pk):

    e = Evaluation.objects.get(id=pk)
    
    context = {"e" : e}
    if request.method == "POST":
        try:
            list1 = request.POST.getlist("subtasks")
            list2 = [x for x in list1 if x != ""]
            subtasks = "\n".join(list2)
        except:
            pass
        #e.update(subtasks=subtasks)
        e.subtasks = subtasks
        e.save()
        print("success")
        return redirect('importantDates')
    return render(request, 'edit_tasks.html', context)


PSI = ['Algoma University','Algonquin College', 'Brock University', 'Cambrian College','Canadore College',
'Carleton University','Centennial College','Collège Boréal (FR)','Conestoga College','Confederation College',
'Durham College','Fanshawe College','Fleming College','George Brown College','Humber College','La Cité collégiale (FR)',
'Lakehead University','Lambton College','Laurentian University','Loyalist College','McMaster University',
'Mohawk College','Niagara College','Nipissing University','Northern College','Northern Ontario School of Medicine (NOSM) University',
'OCAD University','Ontario Tech University','Queen’s University','Royal Military College','Sault College','Seneca College',
'Sheridan College','St. Clair College','St. Lawrence College','Toronto Metropolitan University','Trent University',
'University of Guelph','University of Ottawa','University of Toronto','University of Waterloo','University of Windsor',
'Université de Hearst','Université de l’Ontario français','Western University','Wilfrid Laurier University','York University',
'Other'
] 







#dt = datetime.today()
#used to manually convert to a datetime object from date string to the given format
#dt = datetime.strptime(day, '%Y-%m-%d')

#find start of the week
#dt.weekday() gives position of today's date's current position from Monday 
# timedelta converts to date object so that it can be subtracted from today's date to Monday
#start = dt - timedelta(days=dt.weekday()) 
#add 6 to get Sunday
#end = start +  timedelta(days=6) 
#format date
# weeklyStart = start.strftime('%Y-%m-%d')
# weeklyEnd = end.strftime('%Y-%m-%d')

# weekDateList = []
# for i in range(0,7):
#     j = start + timedelta(days=i)
#     weekDateList.append(j.strftime('%Y-%m-%d'))
 
# print(weekDateList)
 


# 14 days starting from the monday 
# biWeeklyStart = start
# biWeeklyEnd = start + timedelta(days=13)
# #format date
# biWeeklyStart = biWeeklyStart.strftime('%Y-%m-%d')
# biWeeklyEnd = biWeeklyEnd.strftime('%Y-%m-%d')


# month = dt.month
# year = dt.year

# biWeeklyDateList = []
# for i in range(0,14):
#     j = dt + timedelta(days=i) 
#     biWeeklyDateList.append(j.strftime('%Y-%m-%d'))
 
# print(biWeeklyDateList)
 

# all the dates in current week + Next week;
 
# biWeeklyDateListOption2 = []
# for i in range(0,14):
#     j = start + timedelta(days=i) 
#     biWeeklyDateListOption2.append(j.strftime('%Y-%m-%d'))
 
# print(biWeeklyDateListOption2)



# fd,ld = calendar.monthrange(dt.year, dt.month)
 
# startMonth = str(dt.year)+ "-"+str(dt.month)+"-01"
# startMonth = datetime.strptime(startMonth, '%Y-%m-%d')
 
# monthDateList = []
# for md in range(ld):
#     j = startMonth + timedelta(days=md)
#     monthDateList.append(j.strftime('%Y-%m-%d'))
 
# print(monthDateList)