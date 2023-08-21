from django.db import models
from django.utils.timezone import now
import datetime
# *********************user  class**********************************
class Demo(models.Model):
    Name=models.CharField('User Name',null=False, max_length=50)
    completename=models.CharField('complete name',null=False,max_length=100)
    Email=models.EmailField('User Email', max_length=254)
    Password=models.CharField('User Password', max_length=50)
    User_Image=models.ImageField(upload_to="media/%y",blank=True, null=True)
    PhoneNo=models.IntegerField('phoneno',default=0)
    Gender= models.CharField('gender',max_length=50,null=False)
    DateOfBirth=models.DateField('dateofbirth',null=True,blank=True)
    User_Type= models.CharField('usertype',max_length=50,null=False)
    City=models.CharField('city',null=False, max_length=50)
    Country=models.CharField('country',null=False, max_length=50)
    AboutMe=models.CharField('aboutme',null=False, max_length=3000)
    Education_type= models.CharField('education_type',max_length=100,null=False)
    Current_Education_Place=models.CharField('current education place',null=False, max_length=1000)
    Current_Education_Date_From=models.DateField(null=True,blank=True)
    Current_Education_Date_To=models.DateField(null=True,blank=True)
    Current_Education_City=models.CharField('educationcity',null=False, max_length=50)
    Current_Education_Country=models.CharField('educationcountry',null=False, max_length=50)
    Interest=models.CharField('interest',null=False, max_length=3000)
    
    
class Followers(models.Model):
    
    whos_following=models.ForeignKey(Demo,on_delete=models.CASCADE)
    to=models.IntegerField(default=0)
    check_follow= models.CharField(max_length=50,blank=True, null=True)
    
    
class Query(models.Model):
    user_id=models.ForeignKey(Demo,on_delete=models.CASCADE)
    Title=models.CharField('Query title',max_length=100)
    Posted_Date=models.DateTimeField( default=now)
    query_type= models.CharField(max_length=50,blank=True, null=True)
    like=models.IntegerField(default=0)
    unlike=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)
    
class CheckReaction(models.Model):
    query_id=models.ForeignKey(Query,on_delete=models.CASCADE)
    user_id=models.IntegerField(default=0)
    
    
    

class RaisedQuery(models.Model):
    user_id=models.ForeignKey(Demo,on_delete=models.CASCADE)
    Title=models.CharField('Query title',max_length=100)
    Posted_Date=models.DateTimeField( default=now)
    query_type= models.CharField(max_length=50,blank=True, null=True)
    
    
    
class Comment(models.Model):
    message=models.TextField('message')
    date_comment=models.DateTimeField( default=now)
    user_id=models.ForeignKey(Demo,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Query,on_delete=models.CASCADE,null=True)
    parent=models.IntegerField(blank=True, null=True)
    
class Notification(models.Model):
    post_id=models.ForeignKey(Query,on_delete=models.CASCADE,null=True)
    show_user=models.ForeignKey(Demo,on_delete=models.CASCADE)
    user_id=models.IntegerField(default=0)
    notification_date=models.DateTimeField( default=now)
    notification_type=models.CharField(max_length=50,blank=True, null=True)