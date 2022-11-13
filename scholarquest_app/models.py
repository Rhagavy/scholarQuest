from ast import mod
from email.policy import default
from tkinter import CASCADE
from django.db import models
import uuid
from django.contrib.auth.models import User, AbstractUser
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator,MaxValueValidator

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# Create your models here.
# class Admin(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
#     firstName = models.CharField(max_length=100,blank=False,null=False)
#     lastName = models.CharField(max_length=100,blank=False,null=False)
#     displayName = models.CharField(max_length=100,blank=False,null=False)
#     #password =
#     def __str__(self):
#         return self.displayName
class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    first_name = models.CharField(max_length=200,blank=False,null=False)
    last_name = models.CharField(max_length=100,blank=False,null=False)
    dateOfBirth = models.DateField(default="1995-01-01")
    postSecondaryInstitution = models.CharField(max_length = 300, default="Brock University")
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class UsageReport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    createdBy = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    dateCreated = models.DateTimeField(auto_now_add=True) 
    TYPE_CHOICES = [('daily','Daily'),('monthly','Monthly'),('institution','Institution')]
    type = models.CharField(max_length=100,blank=False,null=False,choices=TYPE_CHOICES) 
    def __str__(self):
        return self.dateCreated

class Forum(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    title = models.CharField(max_length=200, blank=False,null=False)
    content = RichTextField()
    #owner = models.ForeignKey(User,on_delete="SET_DEFAULT", default="deleted user")
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)
    STATUS_CHOICES = [('deleted','Deleted'),('ok','Ok')]
    status =  models.CharField(max_length = 100,blank=False,null=False,choices=STATUS_CHOICES)
    #should there be is_deleted flag to check if forum should be shown in the first place
    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = RichTextField()
    date = models.DateTimeField(auto_created=True)
    is_reported = models.BooleanField(default=False)
    STATUS_CHOICES = [('deleted','Deleted'),('ok','Ok')]
    status =  models.CharField(max_length = 100,default= 'ok',blank=False,null=False,choices=STATUS_CHOICES)
    def __str__(self):
        return self.date

class ReportedContent(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment,null=True,on_delete=models.DO_NOTHING)
    reportedBy = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=300)
    dateCreated = models.DateTimeField(auto_created=True)
    TYPE_CHOICES = [('comment','Comment'), ('forum','Forum')]
    type = models.CharField(max_length = 50,blank=False,null=False,choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    STATUS_CHOICES = [('deleted','Deleted'),('dismissed','Dismissed')]
    status =  models.CharField(max_length = 50,blank=False,null=False,choices=STATUS_CHOICES)
    
    # def __str__(self):
    #     return self.dateCreated

class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    finalGrade = models.DecimalField(decimal_places=1,max_digits=4,blank=True,null=True, validators=[MinValueValidator(-1),MaxValueValidator(100)], default = -1)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    courseName = models.CharField(max_length=100,blank=False,null=False)
    courseCode = models.CharField(max_length=100,blank=False,null=False)
    numOfCredits = models.IntegerField(blank=False,null=False)
    totalAssignments = models.IntegerField(blank=False,null=False)
    totalMidTerms = models.IntegerField(blank=False,null=False, default=0)
    has_FinalExam = models.BooleanField(default = False, null=False)
    completionProgress = models.IntegerField(blank=False,null=False,validators=[MinValueValidator(0),MaxValueValidator(100)] ,default=0)
    currentGrade = models.DecimalField(decimal_places=1,max_digits=4,blank=False,null=False,validators=[MinValueValidator(-1),MaxValueValidator(100)],default=-1)
    #finalGrade = models.IntegerField(blank=False,null=False,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)
    def __str__(self):
        return self.courseCode

class Evaluation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False)
    TYPE_CHOICES = [('assignment','Assignment'), ('midterm','MidTerm'), ('finalexam','FinalExam')]
    type = models.CharField(max_length = 50,blank=False,null=False,choices=TYPE_CHOICES)
    #before passing subtask to this field, join all the subtask with a seperator (new line character)
    subtasks = models.CharField(max_length = 5000, blank=True,null=True)
    gradeWeight = models.IntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(100)])
    STATUS_CHOICE = [('in-progress', 'In-Progress'),('complete','Complete')]
    status = models.CharField(max_length = 50,blank=False,null=False,choices=TYPE_CHOICES, default='in-progress')
    grade = models.DecimalField(decimal_places=1,max_digits=4,blank=True,null=True, validators=[MinValueValidator(0),MaxValueValidator(100)], default = 0)


class UserTracking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)

@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    print('User just logged in....')
    UserTracking.objects.create(user=user)

''' import datetime as dt
a = "2022-11-10 22:11:08.815651-05"
print(a[0:19])
b = dt.datetime.strptime(a[0:19],'%Y-%m-%d %H:%M:%S')
print(b.second)
a = "2022-11-10 22:11:08.815651-0500"
b = dt.datetime.strptime(a,"%Y-%m-%d %H:%M:%S.%f%z")'''