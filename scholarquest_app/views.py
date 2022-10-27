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
@register.filter(name='split')
def split(value):
    """
        Returns the value turned into a list.
    """
    #chr(10) is the unicode for \n
    # another way: v = list (value.split(chr(10)))
    v = list (value.split('\n'))
    print(v)
    return v
#Don't need this filt since python by default will split by /n

# Create your views here.
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
        print("hi")
        user = authenticate(request,username = email, password = password)
        #send user to their dashboard page
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
        
        if form.is_valid():
            print("form was valid")
            # user = form.save(commit=False)
            # user.username = user.email
            # user.save()
            form.save()
            print("form saved")
    fieldNames = {'first_name':"First Name",'last_name':"Last Name", 'username':"Forum Display Name",'dateOfBirth':"Date of Birth",'postSecondaryInstitution':"Post Secondary Institution", 'email':"Email Address", 'password1':"Password", 'password2':"Re-type Password"}
    return render(request, 'registration/register.html', {"form":form,"fieldNames":fieldNames})


def profilePage(request,pk):
    userProfile = User.objects.get(id=pk)
    context = {'profile':userProfile}
    return render(request, 'profile.html',context)

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
    #PSI = array of Post Secondary Institution 
    context = {'PSI' : PSI}
    #do I need a seperate form with only the particular editable fields?
    return render (request, 'edit_profile.html', context)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['owner','courseName','courseCode', 'numOfCredits','totalAssignments', 'totalMidTerms','has_FinalExam']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['course','date','type','subtasks','gradeWeight']

def courseCreation(request):
    # 'courseName': ['Intro'], 'courseCode': ['COMP1001'], 'numOfCredits': ['4'], 'assignment[1][date]': ['2022-09-13'], 'assignment[1][gradeWeight]': ['20'], 'assignment[1][subTask][]': ['finish page', 'finish title'], 'assignment[2][date]': ['2022-09-05'], 'assignment[2][gradeWeight]': ['4'], 
    # 'assignment[2][subTask][]': ['finish tomorrow']
    print(request.POST)
    print("I was here")
    courseCreationSuccessful = False
    if(request.method == "POST"):
        #check if grade weight is = 100 or less than
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
        
        for i in request.POST.getlist('assignment-counter'):
            totalGradeWeight += int(request.POST["assignment-"+ i +"-gradeWeight"])

        if totalGradeWeight > 100:
            #flash message to create-course page
            messages.error(request, 'Total grade weight for all evaluations can not exceed 100!')
            return render (request, 'create_course.html')



        courseDict = {'courseName': request.POST['courseName'], 
            'courseCode':request.POST['courseCode'],
            'numOfCredits': request.POST['numOfCredits']}

        courseDict["totalAssignments"] = len(request.POST.getlist('assignment-counter'))

        try:
            courseDict["totalMidTerms"] = len(request.POST.getlist('midterm-counter'))
        except:
            courseDict["totalMidTerms"] = 0

        if "has_FinalExam" in request.POST:
            courseDict["has_FinalExam"] = True
        else:
            courseDict["has_FinalExam"] = False
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

def currentCourse(request):
    return render (request, 'current_course.html')

def editCourse(request):
    return render(request, 'edit_course.html')

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def userDash(request):
    return render (request, 'user_dashboard.html')

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