from django import forms
from .models import *

  
class NewQuery_Images(forms.ModelForm):
  
    class Meta:
        model = Demo
        fields = ['Name', 'Password','Email','completename','User_Image','PhoneNo','Gender','DateOfBirth',
                  'User_Type','City','Country','AboutMe','Education_type','Current_Education_Place','Current_Education_Date_From',
                  'Current_Education_Date_To','Current_Education_City','Current_Education_Country','Interest']
        
        
    

  




class SubscribeForm(forms.Form):
    email = forms.EmailField()