from multiprocessing import context
import re
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.template.defaulttags import register
from django import forms


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
    context = {'PSI' : PSI}
    #do I need a seperate form with only the particular editable fields?
    return render (request, 'edit_profile.html', context)
    
def courseCreation(request):
    return render (request, 'create_course.html')

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def userDash(request):
    return render (request, 'user_dashboard.html')

PSI = ['Algonquin College', 'Brock University', 'Algoma University'] 
