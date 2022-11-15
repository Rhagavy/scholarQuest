from genericpath import exists
from logging import exception
from multiprocessing import context
from pyexpat import model
import re
from django.shortcuts import render, redirect
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views

from django.http import HttpResponseNotFound

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.db.models import Count
from calendar import monthrange

import pandas as pd
import seaborn as sns
import numpy as np

from .models import Course, Evaluation, User, UserTracking, UsageReport
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.template.defaulttags import register
from django import forms
from django.contrib import messages
from datetime import datetime, timedelta
import calendar
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
# from django import template
  
# register= template.Library()
#this custom filter is needed to split subtasks based on "\n" character into individual
#subtasks
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

def defaultPage(request,regex1=''):
    return redirect('/')

#home page
def homePage(request):
    return render(request,'index.html')



def loginPage(request,next=''):
    #check to see if user is coming from another page
    print("printing request.GET")
    print(request.GET)
    print("printing request.POST")
    print(request.POST)
    try:
        next = request.GET['next']
    except Exception as e:
        print("printing error")
        print(e)
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
            print(request.POST)
            print("above is request.POST")
            print(user)
            login(request,user)
            if next != '':
                return redirect(next)
            else:
                return redirect('userDash')
        else:
            print('Email or password is incorrect')
            #add flash message  
    context={'next': next}
    return render(request, 'registration/login.html',context)

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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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
    
    return render (request, 'edit_profile.html', context)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['owner','courseName','courseCode', 'numOfCredits','totalAssignments', 'totalMidTerms','has_FinalExam','currentGrade','finalGrade','completionProgress']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['course','date','type','subtasks','gradeWeight','grade']
        
#both serializers are needed to pass json data of course in update course page, 
#so that we can load a student's current courses in the front-end
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    evaluation = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    def get_evaluation(self, obj):
        evaluation_query = Evaluation.objects.filter(course=obj.id)

        #print(evaluation_query)
        serializer = EvaluationSerializer(evaluation_query,many=True)
        #print(serializer.data)
        return serializer.data

@login_required(login_url='/login/')
def create_or_update_course(request,pk=None):
    # 'courseName': ['Intro'], 'courseCode': ['COMP1001'], 'numOfCredits': ['4'], 'assignment[1][date]': ['2022-09-13'], 'assignment[1][gradeWeight]': ['20'], 'assignment[1][subTask][]': ['finish page', 'finish title'], 'assignment[2][date]': ['2022-09-05'], 'assignment[2][gradeWeight]': ['4'], 
    # 'assignment[2][subTask][]': ['finish tomorrow']
    print(request.POST)
    print(request.path)
    #get the page url
    current_url = resolve(request.path_info).url_name
    print(current_url)
    #assign page header so the page title can be changed accordingly
    if current_url == "createCourse":
        pageHeader = "Create Course"
        
    elif current_url == "editCourse":
        pageHeader = "Update Course"
        try:
            course = Course.objects.filter(owner = request.user).get(id=pk)
        except Exception as e:
            return HttpResponseNotFound("Page not found")
        
        courseData = CourseSerializer(course).data
        courseData = JSONRenderer().render(courseData).decode()
        print(courseData)

        context = {'courseData': courseData, 'course': course, 'pageHeader':pageHeader}
        return render(request, 'createCourse_edit.html',context)
    

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
                    finalGrade += (int(request.POST["assignment-"+ i +"-gradeWeight"])/100) * float(request.POST["assignment-"+ i +"-grade"])
                    print("assignmen")
            except:
               pass

        for i in request.POST.getlist('midterm-counter'):
            try:
                if (request.POST["midterm-"+ i +"-grade"]) == "":
                    assignMidtermWithoutGrade = True
                else:
                    evalutionGrades.append(request.POST["midterm-"+ i +"-grade"])
                    completionProgress += int(request.POST["midterm-"+ i +"-gradeWeight"])
                    finalGrade += (int(request.POST["midterm-"+ i +"-gradeWeight"])/100) * float(request.POST["midterm-"+ i +"-grade"])
                    print("midterm")
            except:
               pass

        try:

            if request.POST["finalExamGrade"] != "":
                evalutionGrades.append(request.POST["finalExamGrade"])
                completionProgress += int(request.POST["finalExamGradeWeight"])
                finalGrade += (int(request.POST["finalExamGradeWeight"])/100) * float(request.POST["finalExamGrade"]) 
                print("final exam")
                #set current grade as -1, since a grade for final exam means student has completed course
                currentGrade = -1
            else:
                currentGrade = sum(map(float,evalutionGrades))/len(evalutionGrades)
                finalGrade = -1   
        except Exception as e:
            currentGrade = sum(map(float,evalutionGrades))/len(evalutionGrades)
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
            totalGradeWeight += int(request.POST["finalExamGradeWeight"])
        except:
            pass
        try:
            for j in request.POST.getlist('midterm-counter'):
                totalGradeWeight += int(request.POST["midterm-"+ j +"-gradeWeight"])
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
            messages.error(request, 'Total grade weight for all evaluations must equal 100 grade weight!-Backend')
            returnOnErrors = True
        if returnOnErrors:
            context = {'userData': request.POST}
            return render (request, 'create_course.html',context)


        #add course information into dictionary
        courseDict = {'courseName': request.POST['courseName'], 
            'courseCode':request.POST['courseCode'],
            'numOfCredits': request.POST['numOfCredits'],
            'currentGrade': currentGrade, 'completionProgress' : int(completionProgress),
            'finalGrade' : "".format({":1f"},finalGrade)}
        #get total evaluation amount for each type
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
        if request.POST["courseID"] != '':
            instance = Course.objects.get(id=request.POST["courseID"])
            form = CourseForm(courseDict,instance=instance)
        else:
            form = CourseForm(courseDict)

        
        print("prining course...before")
        print(courseDict)
        #check to see if course entered id valid based on CourseForm form object and assign successful flag
        if form.is_valid():
            print("course valid")
            print(courseDict)
            course = form.save()
            
            courseCreationSuccessful = True
        else:
            courseCreationSuccessful = False
            
        # ---------------------------------
        #dictionary that holds all assignments
        assignmentDict= {}
        assignmentDict['course'] = course.id
        #loop through and add assignment information
        for i in request.POST.getlist('assignment-counter'):
            assignmentDict['date'] = request.POST["assignment-"+ i +"-date"]
            assignmentDict['gradeWeight'] = request.POST["assignment-"+ i +"-gradeWeight"]
            assignmentDict['grade'] = request.POST["assignment-"+ i +"-grade"]
            print("Assignment Grade")
            print(request.POST["assignment-"+ i +"-grade"])
            #all subtasks are added together with a '\n', to indicate start and end points
            try:
                assignmentDict['subtasks'] = "\n".join(request.POST.getlist("assignment-"+ i +"-subTask"))
            except:
                pass

            assignmentDict['type'] = "assignment"
            #assignment is not empty then it's an already existing assignment that needs to be updates
            if request.POST["assignment-"+ i +"-id"] != "":
                instance = Evaluation.objects.get(id=request.POST["assignment-"+ i +"-id"])
                form = EvaluationForm(assignmentDict,instance=instance)
            else:
                form = EvaluationForm(assignmentDict)
            print("assignment Validation")
            print(assignmentDict)
            #check if input fields are valid against model 
            if form.is_valid():
                print("assignment valid")
                
                form.save()
                
        #holds midterm details
        midtermDict ={}
        midtermDict['course'] = course.id
        #loop through all midterms and add information to dictionary
        try:
            for i in request.POST.getlist('midterm-counter'):
                midtermDict['date'] = request.POST["midterm-"+ i +"-date"]
                midtermDict['gradeWeight'] = request.POST["midterm-"+ i +"-gradeWeight"]
                midtermDict['grade'] = request.POST["midterm-"+ i +"-grade"]
                try:
                    midtermDict['subtasks'] = "\n".join(request.POST.getlist("midterm-"+ i +"-subTask"))
                except:
                    pass
                midtermDict['type'] = "midterm"
                
                if request.POST["midterm-"+ i +"-id"] !="":
                    instance = Evaluation.objects.get(id=request.POST["midterm-"+ i +"-id"])
                    form = EvaluationForm(midtermDict,instance=instance)
                    
                else:
                    form = EvaluationForm(midtermDict)
                print("midterm Validation")
                print(midtermDict)
                if form.is_valid():
                    print("midterm valid")
                   
                    form.save()
        except:
            print("no midterm")
        #hold final exam details
        finalExamDict = {}
        finalExamDict['course'] = course.id
        #grab information from POST and store into dictionary
        try:
            if courseDict["has_FinalExam"]:
                finalExamDict['date'] = request.POST["finalExamDate"]
                finalExamDict['gradeWeight'] = request.POST["finalExamGradeWeight"]
                finalExamDict['grade'] = request.POST["finalExamGrade"]
                print("Exam Grade")
                print(request.POST["finalExamGrade"])
                try:
                    finalExamDict['subtasks'] = "\n".join(request.POST.getlist("finalExamMaterial"))
                except:
                    pass
                finalExamDict['type'] = "finalexam"
                if request.POST["finalexam-id"] !="":
                    instance = Evaluation.objects.get(id=request.POST["finalexam-id"])
                    form = EvaluationForm(finalExamDict,instance=instance)
                else:
                    form = EvaluationForm(finalExamDict)
                print("finalExam Validation")
                print(finalExamDict)
                if form.is_valid():
                    print("finalExam valid")
                    
                    form.save()
                    
        except:
            print("no final exam")
        #assign message based on course creation
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

    #pass it as context so page can be updated with appropriate title
    context = {'pageHeader':pageHeader}
    return render (request, 'createCourse_edit.html',context)

#filter returns evaluation based on type given
@register.filter
def get_evaluation_by_type(course,type):

    return course.evaluation_set.filter(type=type)
#
@register.filter
def checking_type(course,type):
    if course.evaluation_set.filter(type=type):
        print(course.courseCode + ":true")
        return True

    else:
        print(course.courseCode + ":false")
        return False

        

#sk is search key
@login_required(login_url='/login/')
def currentCourse(request, sk=""):
    #get courses based on whether search key is empty or not
    if sk == "":
        courses = Course.objects.filter(owner = request.user.id)
    else:
        courses = Course.objects.filter(owner = request.user.id).filter(courseCode__contains=sk)

    context = {'courses': courses}

    return render (request, 'current_course.html',context)

@login_required(login_url='/login/')
def deleteCourse(request,pk=''):
    print(request.POST)
    if pk != '':
        course = Course.objects.get(id=pk)
    
    if request.method =='POST':
        #check which button was clicked since value is passed in POST request
        if 'confirmDeletion' in request.POST:
            course.delete()
            messages.success(request, "{} has been successfully deleted!".format(course.courseCode))
            return redirect('/current-courses/')
        elif 'cancelDeletion' in request.POST:
            messages.success(request, "{} has not been deleted".format(course.courseCode))
            return redirect('/current-courses/')
    #pass the course the user selected to delete   
    context = {'course' : course}

    return render(request, 'delete_course_confirmation.html', context)

#views that are only accessible by admin (staff_member)
#@staff_member_required()
def currentUsageReports(request):
    graph = institution_plot_view()

    context={'chart': graph}

    return render(request, 'usage_report_page.html',context)
#@staff_member_required
def createUsageReport(request):
    return render(request, 'create_usage_report.html')
#@staff_member_required
def deleteUsageReport (request):
    return render(request, 'delete_usage_report.html')



# def editCourse(request,pk):
#     course = Course.objects.filter(owner = request.user).get(id=pk)
    
#     courseData = CourseSerializer(course).data
#     courseData = JSONRenderer().render(courseData).decode()
#     print(courseData)

#     context = {'courseData': courseData, 'course': course}
#     return render(request, 'createCourse_edit.html',context)



@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

@login_required(login_url='/login/')
def userDash(request):
    courses = Course.objects.filter(owner = request.user.id)
    context = {'courses':courses}
    return render (request, 'user_dashboard.html', context)


@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def gpaCalculatorPage(request):
    return render(request, 'gpa_calculator.html')

def get_graph():
 
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph1 = base64.b64encode(image_png)
    graph = graph1.decode('utf-8')
    buffer.close()
    return graph,graph1
 
def institution_plot_view():
    plt.ioff()
    users = User.objects.values('postSecondaryInstitution').annotate(studentCount = Count('postSecondaryInstitution'))
    df = pd.DataFrame(users)
    df.sort_values(["studentCount"],inplace=True,ascending=False)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(8,6))
    bp = sns.barplot(x=df["studentCount"],y=df["postSecondaryInstitution"],orient='h',hue=df["postSecondaryInstitution"], 
    dodge = False,palette= 'Greens_r')
    plt.legend('', frameon=False)
    plt.ylabel("Post Secondary Intitution")
    plt.xlabel("Number of Students")
    print(plt.style.available)
    plt.tight_layout()
    graph = get_graph()
    
    return graph

def daily_login_report(request):
    #.ioff stops plotting graph ontop of eachother
    plt.ioff()
    plt.clf()
    
    #tsToday = time stamp
    tsToday = datetime.today() - timedelta(days = 0)
    loginData = UserTracking.objects.filter(timeStamp__day = tsToday.day).values()
    df = pd.DataFrame(list(loginData))
    if not (df.empty):

        print(df.head())
        #adding hour coloumn extracted from timeStamp coloumn 
        df["hour"] = df.apply(lambda x: x.timeStamp.hour, axis=1)
        #df = df.groupby(["hour"])["hour"].count()
        #get the hour column and count by unique values
        df = df["hour"].value_counts().to_frame().reset_index().set_axis(["hour","count"],axis=1)
    else:
        df["hour"] = pd.Series()
    for i in range(24):
        if i in list(df["hour"]):
            pass
        else:
            df = pd.concat([df,pd.DataFrame( [{"hour":i, "count":0}])])
    df["labels"] = df["hour"].astype(str)+":00"
    
    bp = sns.barplot(x=df["hour"],y=df["count"])
    plt.xticks(labels=df["labels"],ticks=df["hour"],rotation=90,fontsize=9)
    plt.ylim(bottom=0)
    
    plt.ylabel("Login Count")
    plt.xlabel("Hour")

    # print(df.head(22))
    print(df.info())
    # print(df.shape)
    # print(df.tail())
    # print(tsToday)

    plt.tight_layout()
    graph = get_graph()
    context={'chart': graph}
    del df
    return render(request, 'graph.html',context)

def monthly_login_report(request):
    #.ioff stops plotting graph ontop of eachother
    plt.ioff()
    plt.clf()
    
    #tsToday = time stamp
    tsToday = datetime.today() - timedelta(days = 260)
    loginData = UserTracking.objects.filter(timeStamp__month = tsToday.month).values()
    df = pd.DataFrame(list(loginData))
    if not (df.empty):

        
        #adding hour coloumn extracted from timeStamp coloumn 
        df["day"] = df.apply(lambda x: x.timeStamp.day, axis=1)
        
        #df = df.groupby(["hour"])["hour"].count()
        #get the hour column and count by unique values
        df = df["day"].value_counts().to_frame().reset_index().set_axis(["day","count"],axis=1)
        print(df.head(30))
    else:
        df["day"] = pd.Series()
    #monthrange will get output tuple: (first week day of month, # number of days in month)
    xTicks = np.arange(1,monthrange(tsToday.year,tsToday.month)[1]+1,1)
    print(xTicks)
    for i in xTicks:
        if i in list(df["day"]):
            pass
        else:
            df = pd.concat([df,pd.DataFrame( [{"day":i, "count":0}])])
    df["day"] = df["day"].astype(int)
    print(df.info())
    bp = sns.barplot(x=df["day"],y=df["count"])
    plt.xticks(fontsize=9)
    plt.ylim(bottom=0)
    
    plt.ylabel("Login Count")
    plt.xlabel("Month")

    # print(df.head(22))
    print(df.info())
    # print(df.shape)
    # print(df.tail())
    # print(tsToday)

    plt.tight_layout()
    graph = get_graph()
    context={'chart': graph}
    del df
    return render(request, 'graph.html',context)

def weekly_login_report(request):
    #.ioff stops plotting graph ontop of eachother
    plt.ioff()
    plt.clf()
    
    #tsToday = time stamp
    tsToday = datetime.today() - timedelta(days = 1)
    loginData = UserTracking.objects.filter(timeStamp__week = tsToday.isocalendar()[1]).values()
    df = pd.DataFrame(list(loginData))
    if not (df.empty):

        
        #adding day coloumn extracted from timeStamp coloumn 
        df["day"] = df.apply(lambda x: x.timeStamp.day, axis=1)
        
        #df = df.groupby(["hour"])["hour"].count()
        #get the day column and count by unique values
        df = df["day"].value_counts().to_frame().reset_index().set_axis(["day","count"],axis=1)
        print(df.head(30))
    else:
        df["day"] = pd.Series()
    df["label"] = pd.Series()

    start = tsToday - timedelta(days=tsToday.weekday()) 
    xTicks= []
    for i in range(7):
        xTicks.append(start+timedelta(days=i))

    print(xTicks)
    for i in xTicks:
        if i.day in list(df["day"]):
            df.loc[df['day'] == i.day, 'label'] = i.strftime('%d-%m-%Y')
        else:
            df = pd.concat([df,pd.DataFrame( [{"day":i.day, "count":0,"label":i.strftime('%d-%m-%Y')}])])
    df.sort_values(["label"],inplace=True)
    #df["day"] = df["day"].astype(int)
    print(df.info())
    bp = sns.barplot(x=df["label"],y=df["count"])
    plt.xticks(fontsize=9, rotation = 45)
    plt.ylim(bottom=0)
    
    plt.ylabel("Login Count")
    plt.xlabel("Day of the Week")

    # print(df.head(22))
    print(df.info())
    # print(df.shape)
    # print(df.tail())
    # print(tsToday)

    plt.tight_layout()
    graph,buffer = get_graph()
    #UsageReport.objects.create(createdBy=request.user,type='weekly',graphImage = buffer)
    qs = UsageReport.objects.get(id="2f5a4913-84dc-4ad6-a697-c142302cff42")
    finalImage=base64.b64encode(qs.graphImage).decode('utf-8')
    context={'chart': finalImage}
    return render(request, 'graph.html',context)

"""
dict1 = [{"a":"23","b":3},{"a":"8","b":2},{"a":"df","b":7},{"a":"skl","b":40}]
df=pd.DataFrame()
df = pd.DataFrame(dict1)
print(df.head())
df.sort_values(["b"],inplace=True,ascending=False)
bp = sns.barplot(x=df["b"],y=df["a"],orient='h',hue=df["a"], dodge = False,palette= 'Greens_r')
# bp.invert_yaxis()
bp.legend(loc='upper right', bbox_to_anchor=(1.16, 1),borderaxespad=0)
plt.tight_layout()
plt.savefig("graph.png",format="png")

"""



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