from django.db import models

# Create your models here.

class LoginModel(models.Model):
    Username = models.CharField(max_length=100, null=True, blank=True)  
    Password = models.CharField(max_length=100, null=True, blank=True)
    UserType = models.CharField(max_length=100, null=True, blank=True)

    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_verified = models.BooleanField(default=False)



class UserModel(models.Model):
    LOGINID = models.ForeignKey(LoginModel, on_delete=models.CASCADE, null=True, blank=True)
    FullName = models.CharField(max_length=100, null=True, blank=True)    
    Email = models.CharField(max_length=100, null=True, blank=True)    
    Phone = models.BigIntegerField(null=True, blank=True)    
    Address = models.TextField(null=True, blank=True)    
    Gender = models.CharField(null=True, blank=True, max_length=100)    

class FeedbackModel(models.Model):
    feedback= models.CharField(max_length=100, null=True, blank=True)
    USERID= models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True) 

class complaintsModel(models.Model):
    USERID= models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True) 
    Complaint=models.TextField(max_length=100,null=True,blank=True)
    Reply=models.CharField(max_length=100,null=True,blank=True)  


class DailyActivities(models.Model):
    USERID = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    mood = models.CharField(max_length=100, null=True, blank=True)
    Day = models.DateField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

class ExpenseTable(models.Model):
    USERID = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    Day = models.DateField(null=True, blank=True)
    ExpenseType = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Amount = models.FloatField(null=True, blank=True)


class SalaryTable(models.Model):
    USERID = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    Day = models.DateField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)


class ReminderModel(models.Model):
    USERID = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    Date = models.DateField(null=True, blank=True)
    Time = models.TimeField(null=True, blank=True)
    Reminder = models.TextField(null=True, blank=True)