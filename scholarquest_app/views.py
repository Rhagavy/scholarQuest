from django.shortcuts import render, redirect
from django.forms import ModelForm
from .models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def homePage(request):
    return render(request,'index.html')

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('homePage')

    if request.method == 'Post':
        
        print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        #validate
        try:
            user = User.objects.get(email = email)
        except:
            print( 'Email does not exist')
            #add flash message

        user = authenticate(request,username = email, password = password)
        #send user to their dashboard page
        if user is not None:
            print(user)
            login(request,user)
            return redirect('home')
        else:
            print('Email or password is incorrect')
            #add flash message  
    return render(request, 'login.html')

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
    return render(request, 'register.html', {"form":form,"fieldNames":fieldNames})

def profilePage(request):
    return render(request, 'profile.html')


