from pickle import FALSE
from threading import local
from urllib.request import Request
from django import http
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from joblib import PrintTime
from numpy import empty
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import string    
import random
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import re
x_x=0
def signup(request):
    return render(request, "signup.html",{'signup':1})
@csrf_exempt
def adminprofile(request):
    labels = []
    data = []
    hot_trends = TrendsTopic.objects.all()[:5]
    for i in hot_trends:
        labels.append(i.query_type)
        data.append(i.count)

    print(labels)
    # print(data)
    if request.POST:
      
     user_id = request.session['user_id']
     message=request.POST.get('message')
      
     print(message)
     message_tag=request.POST.get('message_tag')
     obj = RaisedQuery(Title=message,query_type=message_tag)
     obj.user_id_id = user_id
     obj.save()
    else:
            
            
            
           
 
        
            userid = request.session['user_id']
            data = Demo.objects.get(id=userid)
            fetch_data = RaisedQuery.objects.all().order_by('-Posted_Date')
            comment = Comment.objects.all()
            replycomment = Comment.objects.all()
            comment_count = Comment.objects.all().count()
           
            return render(request, 'adminprofile.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'admin':1 })

 

def login(request):
    if request.POST:
        
        user_email = request.POST['useremail']
       
        user_type=request.POST['user_change']
        
        user_password = request.POST['userpassword']
      
        if user_type == "admin":
            
            countt = Demo.objects.filter(Email=user_email,Password=user_password).count()
            if countt>0:
               return redirect('adminprofile')
            else:
                messages.error(request, 'You Enter Wrong Email | Password!')
                return redirect('login')
        else:   
         count = Demo.objects.filter(Email=user_email).count()
         if count > 0:
        
          check_password_using_email = Demo.objects.values('Password').filter(Email=user_email)[0]
          UserPassword_check=check_password(user_password,check_password_using_email['Password'])
          
          
          if UserPassword_check == True:
    
            request.session['is_logged'] = True
            request.session['user_id'] = Demo.objects.values('id').filter(
                Email=user_email)[0]['id']
            
            return redirect('home')
          else:
            value={
                'user_email':user_email
            }
            messages.error(request, 'Invalid Password ')
            return render(request,'login.html',{'email_user':value})
         else:
            messages.error(request, 'Invalid Email')
            return redirect('login')
    else:
        return render(request, "login.html")   
def newRegestrations(request):
   
    if request.POST:
        complete_username = request.POST['completename']
        user_name=request.POST['name']
        useremail = request.POST['email']
        userpassword = request.POST['password']
        
        temp_password=userpassword
        userpassword=make_password(userpassword)
        phoneno=request.POST['phoneno']
        gender=request.POST['gender']
        dob=request.POST['dob']
        usertype=request.POST['usertype']
        usercity=request.POST['usercity']
        usercountry=request.POST['usercountry']
        useraboutme=request.POST['useraboutme']
        educationtype=request.POST['educationtype']
        currentuni=request.POST['currentuni']
        current_edu_from=request.POST['current_edu_from']
        current_edu_to=request.POST['current_edu_to']
        edu_city=request.POST['edu_city']
        edu_country=request.POST['edu_country']
        user_interest=request.POST['user_interest']
        value={
                "complete_username":complete_username,
                "user_name":user_name,
                "useremail":useremail,
                "phoneno":phoneno,
                "usercity":usercity,
                "usercountry":usercountry,
                "currentuni":currentuni,
                "edu_city":edu_city,
                "edu_country":edu_country
      
            }
        
        for_check_account = Demo.objects.filter(Email=useremail).count()
        check_complete_name=0
        
        if len(temp_password) < 3 and for_check_account>0:
            if len(complete_username) >5:
              
             for character in complete_username:
    

              if character.isdigit():
               check_complete_name=check_complete_name+1
               if check_complete_name > len(complete_username)/2:
                  
                 msg="*Your Name Contain too much numbers"
                 messages.error(request, 'This Email is Already Regestred!')
                 msg2="*Your Password Length is Less then 3"
                 return render(request, 'signup.html', {'psd_msg':msg2,'msg':msg,'value':value} )
            else:
                
                msg="*Your Name must be of length 5"
                messages.error(request, 'This Email is Already Regestred!')
                msg2="*Your Password Length is Less then 3"
                return render(request, 'signup.html', {'psd_msg':msg2,'msg':msg,'value':value} )
        
        
        elif len(temp_password) < 3 :
            if len(complete_username) >5:
             for character in complete_username:
    

              if character.isdigit():
               check_complete_name=check_complete_name+1
               if check_complete_name == len(complete_username)/2:
                   msg="*Your Name Contain too much numbers"
                   msg2="*Your Password Length is Less then 3"
                   return render(request, 'signup.html', {'psd_msg':msg2,'msg':msg,'value':value} )
            else:
                msg="*Your Name must be of length 5"
                msg2="*Your Password Length is Less then 3"
                return render(request, 'signup.html', {'psd_msg':msg2,'msg':msg,'value':value} )
                
           
                   
           
            
        
        
        
                  
       
        
        
        
        
        if for_check_account == 0:
            if request.FILES.get('image'):
                user_image = request.FILES['image']

                fss = FileSystemStorage()
                file = fss.save(user_image.name, user_image)
                file_url = fss.url(file)
                obj = Demo(Name=user_name,completename=complete_username,Email=useremail, Password=userpassword,User_Image=user_image,
                           PhoneNo=phoneno,Gender=gender,DateOfBirth=dob,User_Type=usertype,City=usercity,Country=usercountry,
                           AboutMe=useraboutme,Education_type=educationtype,Current_Education_Place=currentuni,
                           Current_Education_Date_From=current_edu_from,Current_Education_Date_To=current_edu_to,
                           Current_Education_City=edu_city,Current_Education_Country=edu_country,Interest=user_interest)
                obj.save()
                messages.success(request, 'Sucessfully Regestred!')
                return redirect('login')
            else:
                obj = Demo(Name=user_name,completename=complete_username,Email=useremail, Password=userpassword,
                           PhoneNo=phoneno,Gender=gender,DateOfBirth=dob,User_Type=usertype,City=usercity,Country=usercountry,
                           AboutMe=useraboutme,Education_type=educationtype,Current_Education_Place=currentuni,
                           Current_Education_Date_From=current_edu_from,Current_Education_Date_To=current_edu_to,
                           Current_Education_City=edu_city,Current_Education_Country=edu_country,Interest=user_interest)
                obj.save()
                messages.success(request, 'Sucessfully Regestred!')
                return redirect('login')
        elif for_check_account>0:
            messages.error(request, 'This Email is Already Regestred!')
            return redirect('login')

def search_post(request):
    if request.session.has_key('is_logged'):
            if request.POST:
               
               query = request.POST['search_profile']
               
               allposts = Demo.objects.filter(completename__icontains=query)
               
               userid=request.session['user_id']
               profile_id=request.POST.get('profile_idd')
               followers_data=Followers.objects.filter(whos_following=userid)
               data = Demo.objects.get(id=userid)
               q=request.GET.get('q')
               follow_data = Followers.objects.filter(to=userid).all()
               fetch_data = Query.objects.all().order_by('-Posted_Date')
               
               comment = Comment.objects.all()
               replycomment = Comment.objects.all()
               comment_count = Comment.objects.all().count()
               follow_data_count = Followers.objects.filter(to=userid).all().count()
               hot_trends = TrendsTopic.objects.all().order_by('-count')
               if len(query) == 0:
                    
                    allposts = Demo.objects.all()
                    
                    return render(request, 'home.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data ,'follow_data_count':follow_data_count,'trends':hot_trends})

                   
               if allposts.count() == 0:
                 
                 messages.warning(request, "No Search Found!")
               
                 return render(request, 'home.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,'follow_data_count':follow_data_count,'trends':hot_trends })
               else:
                 
                 return render(request, 'home.html', {'dataa': fetch_data,'data': allposts,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,"t":1 ,'follow_data_count':follow_data_count,'trends':hot_trends})
     
    else:
     return redirect('login')

             

def home(request):
   
    if request.session.has_key('is_logged'):
            if request.POST:
               
               query = request.POST['search']
               allposts_Titles = Query.objects.filter(Title__icontains=query)
               
               
               allposts_type = Query.objects.filter(query_type__icontains=query)
               allposts = allposts_Titles.union(allposts_type).order_by('-Posted_Date')
               userid=request.session['user_id']
               profile_id=request.POST.get('profile_idd')
               followers_data=Followers.objects.filter(whos_following=userid)
               data = Demo.objects.get(id=userid)
               q=request.GET.get('q')
               follow_data = Followers.objects.filter(to=userid).all()
               follow_data_count = Followers.objects.filter(to=userid).all().count()
               hot_trends = TrendsTopic.objects.all().order_by('-count')
              
               fetch_data = Query.objects.all().order_by('-Posted_Date')
              
               check_rection=CheckReaction.objects.filter(user_id=userid)
               comment = Comment.objects.all()
               replycomment = Comment.objects.all()
               comment_count = Comment.objects.all().count()
               
               fetch_notification = Notification.objects.filter(user_id=userid).all().order_by('-notification_date')
               fetch_notification_count=Notification.objects.filter(user_id=userid).all().count()
               
               if allposts.count() == 0:
                 messages.warning(request, "Please enter correct data for proper search!")
               
                 return render(request, 'home.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,'check_rection':check_rection,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count,'follow_data_count':follow_data_count,'trends':hot_trends })
               else:
                 return render(request, 'home.html', {'dataa': fetch_data,'data': allposts,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,'check_rection':check_rection,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count,'follow_data_count':follow_data_count,'trends':hot_trends})
              
            else:
             userid=request.session['user_id']
             profile_id=request.POST.get('profile_idd')
            
             
             followers_data=Followers.objects.filter(whos_following=userid)
             follow_data_count = Followers.objects.filter(to=userid).all().count()
             data = Demo.objects.get(id=userid)
             q=request.GET.get('q')
             check_rection=CheckReaction.objects.filter(user_id=userid)
          
             hot_trends = TrendsTopic.objects.all().order_by('-count')  
             
             follow_data = Followers.objects.filter(to=userid).all()
             fetch_data = Query.objects.all().order_by('-Posted_Date')
            
             comment = Comment.objects.all()
             replycomment = Comment.objects.all()
             comment_count = Comment.objects.all().count()
             fetch_notification = Notification.objects.filter(user_id=userid).all().order_by('-notification_date')
             fetch_notification_count=Notification.objects.filter(user_id=userid).all().count()
           
             if q == None:
 
                 return render(request, 'home.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,'check_rection':check_rection,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count,'follow_data_count':follow_data_count,'trends':hot_trends })
             else:
                 fetch_data = Query.objects.filter(query_type=q).all().order_by('-Posted_Date')
                 return render(request, 'home.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,'check_rection':check_rection,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count,'follow_data_count':follow_data_count,'trends':hot_trends})
 
     
    else:
     return redirect('login')



def logout(request):
     del request.session['is_logged']
     return redirect('login')
   


# ***********************nlp*********************
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def preprocess(sentence):
    # convert message to string
    sentence = str(sentence)
    # convert message to lowercase
    sentence = sentence.lower()
    #replace '{html}' word from text with  " "
    sentence = sentence.replace('{html}', "")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url = re.sub(r'http\S+', '', cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)
    
    filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
    stem_words = [stemmer.stem(w) for w in filtered_words]
    lemma_words = [lemmatizer.lemmatize(w) for w in stem_words]
    return filtered_words
def trend_topic_count(topic):

   
    check_already=TrendsTopic.objects.filter(query_type=topic)
    if check_already:
    
     if check_already[0].count >= 1:
       
     
       dummy=TrendsTopic.objects.filter(query_type=topic)
       obj = TrendsTopic.objects.filter(query_type=topic).update(count=dummy[0].count + 1 )
    else:
        obj2=TrendsTopic(query_type=topic,count=1)
        obj2.save()


def new_query(request):
 
  if request.session.has_key('is_logged'): 
    if request.POST:
        new_list=[]
        if request.POST['title']:
         user_title = request.POST['title']
         new_list=preprocess(user_title)
         new_list = list(dict.fromkeys(new_list))
        #  print nlp extracted words***********************************************
        #  print(new_list)
         
        else:
            if 'http://127.0.0.1:8000/' == request.META.get('HTTP_REFERER'):
                 return redirect('home')
            elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
              return redirect('timeline')
        if request.POST.get('querytype'):
         querytype=request.POST['querytype']
         trend_topic_count(querytype)
         
        
        else:
             
             if 'http://127.0.0.1:8000/' == request.META.get('HTTP_REFERER'):
              return redirect('home')
             elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
              return redirect('timeline')
          
          
        f = open('misuse.txt')
        content = f.read()
        listt = content.split()
        # final_list contain words that are come after NLP process
        final_list= new_list
        
        # for user_name check misuse detect
        percentage=0
        length_of_extracted_words=len(new_list)
        count_misuse=0;
        for i in listt:

            for n in final_list:
                if i == n:
                    count_misuse=count_misuse+1
                    continue
        if length_of_extracted_words>0:
         percentage=count_misuse/length_of_extracted_words*100
        
        
        else:
                    messages.warning(request,  'please Enter Proper Query')
                   
                    if 'http://127.0.0.1:8000/' == request.META.get('HTTP_REFERER'):
                     return redirect('home')
                    elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
                      return redirect('timeline')
                    else:
                     return redirect('home')
        
        if percentage >= 50:
                       messages.warning( request,  'please do not enter FALSE information')
                    
                       userid=request.session['user_id']
                       profile_id=request.POST.get('profile_idd')
                       followers_data=Followers.objects.filter(whos_following=userid)
                       data = Demo.objects.get(id=userid)
                       q=request.GET.get('q')
                       check_rection=CheckReaction.objects.filter(user_id=userid)
           

                       follow_data = Followers.objects.filter(to=userid).all()
                       fetch_data = Query.objects.all().order_by('-Posted_Date')
                       comment = Comment.objects.all()
                       replycomment = Comment.objects.all()
                       comment_count = Comment.objects.all().count()
                       fetch_notification = Notification.objects.filter(user_id=userid).all().order_by('-notification_date')
                       fetch_notification_count=Notification.objects.filter(user_id=userid).all().count()
           
                       if 'http://127.0.0.1:8000/timeline' != request.META.get('HTTP_REFERER'):
 
                          return render(request, 'home.html', {'dataa': fetch_data,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'follow_data':follow_data,'follower_data':followers_data,'check_rection':check_rection,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count,"query_false":1 })           
                   
                        
                        
                       elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
                          return redirect('timeline')
                       else:
                          return redirect('home')
        else:
                if  user_title:
                  user_id = request.session['user_id']
                  obj = Query(Title=user_title,query_type=querytype)
                #   obj = QueryTypeCount(query_type=querytype)
                  
                  
                  obj.user_id_id = user_id
                  
                  obj.save()
                  if 'http://127.0.0.1:8000/' == request.META.get('HTTP_REFERER'):
                   return redirect('home')
                  elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
                   return redirect('timeline')
            

                else:

                  if 'http://127.0.0.1:8000/' == request.META.get('HTTP_REFERER'):
                   return redirect('home')
                  elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
                   return redirect('timeline')

    else:
        if 'http://127.0.0.1:8000/' == request.META.get('HTTP_REFERER'):
         return redirect('home')
        elif 'http://127.0.0.1:8000/timeline' == request.META.get('HTTP_REFERER'):
          return redirect('timeline')
  else:
     return redirect('login')
        # ****************add comment using ajax**************************
@csrf_exempt
def readmore(request):
   
    
 if request.session.has_key('is_logged'): 
    
    if request.POST:
        message = request.POST.get('comment_value')
       
        if len(message) > 0:
            
            user_id = request.POST.get('user_id')
            post_id = request.POST.get('post_id')
            type = request.POST.get('type')
            user_who_posted=request.POST.get('user_who_posted')
            add_comment = Comment(message=message)
            add_comment.post_id_id = post_id
            obj = Query.objects.filter(id=request.POST.get('post_id')).update(comment_count= add_comment.post_id.comment_count + 1)
            add_comment.user_id_id = user_id
            add_comment.save()
            if user_id!=user_who_posted:
             obj2=Notification(user_id=user_who_posted,notification_type=type)
             obj2.post_id_id = post_id
             obj2.show_user_id = user_id
             obj2.save()
            
            if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
             return redirect('home')
            elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
             return redirect('timeline')
        elif len(message)==0:
             if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
              return redirect('home')
             elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
              return redirect('timeline') 

 else:
     return redirect('login')
 

    
@csrf_exempt
def delete_post(request):
    id=request.POST.get('post_id')
    type=request.POST.get('trend_topic')
    
    dummy=TrendsTopic.objects.filter(query_type=type)
    obj = TrendsTopic.objects.filter(query_type=type).update(count=dummy[0].count - 1 )
    Query.objects.filter(id=id).delete()
    if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
     return redirect('home')
    elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
      
      return redirect('timeline')

@csrf_exempt
def raised_post_delete(request):
    
    id=request.POST.get('post_id')
    RaisedQuery.objects.filter(id=id).delete()
    forget_email=request.POST.get('email')
    subject='Post Declined'
    message='You are receiving this e-mail because your Post Is Declined By Our Admin.The Post Contain False Information  '
   
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [forget_email] 
    fail_silently=False
    send_mail( subject, message, email_from,recipient_list,fail_silently )
    return redirect('adminprofile')

     
@csrf_exempt
def delete_comment(request):
   id=request.POST.get('post_id')
   i=request.POST.get('i')
   Comment.objects.filter(id=id).delete()
   dummy=Query.objects.filter(id=i)
   obj = Query.objects.filter(id=i).update(comment_count=dummy[0].comment_count - 1 )
   if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
         return redirect('home')
   elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
      return redirect('timeline')


def update_post(request, id):
    data = Query.objects.get(id=id)
    return render(request, 'update_post.html', {'DATA': data, 'ID': id})


@csrf_exempt
def updated_query(request):
   

        user_title = request.POST.get('message')
        user_id =request.POST.get('user_id')
        post_id = request.POST.get('post_id')

        if  user_title:
            obj = Query.objects.filter(id=post_id).update(
                                                     Title=user_title)
            if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
             return redirect('home')
            elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
             return redirect('timeline')
        else:
            if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
             return redirect('home')
            elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
             return redirect('timeline')



 #for reply comment
def reply_comment(request):
 if request.session.has_key('is_logged'): 
    if request.POST:
        replymessage = request.POST['reply_message']
        user_id = request.POST['user_id']
        post_id = request.POST['reply_id']
        
        add_comment = Comment(message=replymessage)
        add_comment.parent = post_id
        add_comment.user_id_id = user_id
        
        add_comment.save()

        if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
         return redirect('home')
        elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
           return redirect('timeline')
 else:
     return redirect('login')
 
 #for update comment
@csrf_exempt
def update_comment(request):
 if request.session.has_key('is_logged'): 
    id=request.POST.get('post_id')
    if request.POST:
        updated_comment =  request.POST.get('message')
        if len(updated_comment) == 0:
            if 'http://127.0.0.1:8000/' ==request.META.get('HTTP_REFERER'):
               return redirect('home')
            elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
               return redirect('timeline')

        else:
            obj = Comment.objects.filter(id=id).update(message=updated_comment)
            if 'http://127.0.0.1:8000/home' ==request.META.get('HTTP_REFERER'):
              return redirect('home')
            elif 'http://127.0.0.1:8000/timeline' ==request.META.get('HTTP_REFERER'):
             return redirect('timeline')
 else:
      return redirect('login')
 #for forget passoword
def forgetpassword(request):
  
    if request.POST:
      forget_email=request.POST['email']
      count = Demo.objects.filter(
            Email=forget_email).count()
    
      if count==0:
         messages.error(request,"Make Sure You Enter Correct Email ")
         return redirect('login')
      elif count >0:
       S = 6  # number of characters in the string.
       ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) # generate random string
       ran_encrypted=make_password(ran)
       obj = Demo.objects.filter(Email=forget_email).update(Password=ran_encrypted) 
       subject='Password reset'
       message='You are receiving this e-mail because you requested a password reset for your user account at Expert Academic Portal..'
       message_password='you temporary password is:'+ ran
       email_from = settings.EMAIL_HOST_USER
       recipient_list = [forget_email] 
       fail_silently=True
       send_mail( subject, message+message_password, email_from, recipient_list,fail_silently )
       messages.error(request, 'Please Check Your Given Email ')
       return redirect('login')
    else:
      return render(request, "forgetpassword.html")

   #for change passowrd
def changepassword(request):
 if request.session.has_key('is_logged'):    
  if request.POST:
    user_id=request.session['user_id']
    new_password=request.POST['newpassword']
    old_details=Demo.objects.filter(id=user_id).all()
    confirm_password=request.POST['confirmpassword']
    old_password = Demo.objects.get(id = user_id)
    
    check_password_using_email = Demo.objects.values('Password').filter(id=user_id)[0]
    UserPassword_check=check_password(new_password,check_password_using_email['Password'])
    
    if UserPassword_check == True:
         messages.error(request, "Your Enter Old Password!")
         return render(request, "changepassword.html",{"check":1})

    
    elif new_password!=confirm_password:
        messages.error(request, "Please Enter Both Passwords Same")
        return render(request, "changepassword.html",{"check":1})
        
    else:
        password_encrypted=make_password(new_password)
        obj = Demo.objects.filter(id=user_id).update(Password=password_encrypted)
        messages.info(request, "Your Password is Changed!")
        return render(request, "changepassword.html")
        
  else:
      
        return render(request, "changepassword.html",{"check":1})
    
 else:
     return redirect('login')
 
  #for timeline page
@csrf_exempt
def timeline(request):
     
      
      if request.session.has_key('is_logged'):
          
            
            userid=request.session['user_id']
            profile_id=request.POST.get('profile_idd')
           
            if profile_id == None:
            
             userid=request.session['user_id']
             follow_data = Followers.objects.filter(to=userid).all()
             data = Demo.objects.get(id=userid)
             fetch_data = Query.objects.filter(user_id=userid).all().order_by('-Posted_Date')
             fetch_dataa = Query.objects.all().order_by('-Posted_Date')
             comment = Comment.objects.all()
             replycomment = Comment.objects.all()
             comment_count = Comment.objects.all().count()
             count_followers=Followers.objects.filter(to=userid).count()
             fetch_notification = Notification.objects.filter(user_id=userid).all().order_by('-notification_date')
             fetch_notification_count=Notification.objects.filter(user_id=userid).all().count()
             follow_data_count = Followers.objects.filter(to=userid).all().count()
             hot_trends = TrendsTopic.objects.all().order_by('-count')
             return render(request, 'timeline.html', {'dataa': fetch_dataa,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':data,'count_followers':count_followers,'follow_data':follow_data,'timeline_check':True,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count ,'follow_data_count':follow_data_count,'trends':hot_trends })
            else:
             followers_data=Followers.objects.filter(to=profile_id ,whos_following=userid)
             follow_data = Followers.objects.filter(to=userid).all()
             count_followers=Followers.objects.filter(to=profile_id).count()
             data = Demo.objects.get(id=profile_id)
             currentid =request.session['user_id']
             current_user_data=Demo.objects.get(id=currentid)
             fetch_data = Query.objects.filter(user_id=profile_id).all().order_by('-Posted_Date')
             fetch_dataa = Query.objects.all().order_by('-Posted_Date')
             comment = Comment.objects.all()
             replycomment = Comment.objects.all()
             comment_count = Comment.objects.all().count()
             fetch_notification = Notification.objects.filter(user_id=userid).all().order_by('-notification_date')
             fetch_notification_count=Notification.objects.filter(user_id=userid).all().count()
             follow_data_count = Followers.objects.filter(to=userid).all().count()
             hot_trends = TrendsTopic.objects.all().order_by('-count')
             return render(request,'timeline.html', {'dataa': fetch_dataa,'data': fetch_data,'user_data':data, 'ID': userid,'comment': comment,'COUNT':comment_count,'REPLY':replycomment,'currentid':current_user_data,'count_followers':count_followers,'follow_data':follow_data,'follower_data':followers_data,'timeline_check':True,'fetch_notification':fetch_notification,'fetch_notification_count':fetch_notification_count,'follow_data_count':follow_data_count,'trends':hot_trends })
                
      else:
        return redirect('login')
    #for profile image
def userimage(request,id):
   if request.POST: 
     img=request.POST.get('image')
     
     if img:
                user_image = request.POST['image']
        
    
                obj = Demo.objects.filter(id=id).update(User_Image=user_image)
                return redirect('timeline')
     else:
        return redirect('timeline')
   else:
     return redirect('login')   

@csrf_exempt
def like(request):
    
    id=request.POST.get('post_id')
    userid=request.POST.get('userid')
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')
    type = request.POST.get('type')
    user_who_posted=request.POST.get('user_who_posted')

    if user_id!=user_who_posted:
     obj2=Notification(user_id=user_who_posted,notification_type=type)
     obj2.post_id_id = post_id
     obj2.show_user_id = user_id
     obj2.save()
     
    dummy=Query.objects.filter(id=id)
    like_count=dummy[0].like + 1
    
    obj = Query.objects.filter(id=id).update(like=like_count )
    obj2 = CheckReaction(user_id=user_id)
    obj2.query_id_id = id
    obj2.save()
    return JsonResponse()
@csrf_exempt   
def dislike(request):
    id=request.POST.get('post_id')
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')
    type = request.POST.get('type')
    user_who_posted=request.POST.get('user_who_posted')
    
    if user_id!=user_who_posted:
     obj2=Notification(user_id=user_who_posted,notification_type=type)
     obj2.post_id_id = post_id
     obj2.show_user_id = user_id
     obj2.save()
    dummy=Query.objects.filter(id=id)
    obj = Query.objects.filter(id=id).update(unlike=dummy[0].unlike + 1 )
    return JsonResponse()

@csrf_exempt
def follow(request):
    
    user_id=request.POST.get('user_id')
    current_id=request.POST.get('current_id')
    check=request.POST.get('CHECK_FOLLOW')
    
   
    if check == 'UnFollow':
      
     obj = Followers(to=user_id,check_follow=check)
     obj.whos_following_id = current_id
     obj.save()
     
    elif check=='Follow':
     Followers.objects.filter(whos_following = current_id,to=user_id).delete()
     
  
    return redirect('home')



@csrf_exempt
def approved_post(request):
    
   
    Raised_Query=request.POST.get('RaisedQuery')
    RaisedQueryTag=request.POST.get('RaisedQueryTag')
    user_id = request.POST.get('userId')
    obj = Query(Title=Raised_Query,query_type=RaisedQueryTag)
    obj.user_id_id = user_id
    obj.save()
    
    
    postid=request.POST.get('post_id')
    RaisedQuery.objects.filter(id=postid).delete()
    
    forget_email=request.POST.get('email')
   
    subject='Post Approved'
    message='You are receiving this e-mail because your Post Is Approved By Our Admin.'
   
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [forget_email] 
    fail_silently=False
    send_mail( subject, message, email_from,recipient_list,fail_silently )
    
    return redirect('adminprofile')

def edit(request):
 if request.session.has_key('is_logged'):
     q=request.GET.get('vl')
     userid=request.session['user_id']
     data = Demo.objects.get(id=userid)
     user_id=request.session['user_id'] 
     if q == "1" :
       
       if request.POST:
        
         
        complete_username = request.POST['completename']
        user_name=request.POST['name']
        useremail = request.POST['email']
        phoneno=request.POST['phoneno']
        gender=request.POST['gender']
        dob=request.POST['dob']
        usertype=request.POST['usertype']
        usercity=request.POST['usertype']
        usercountry=request.POST['usercountry']
        useraboutme=request.POST['useraboutme']
        
        
        obj = Demo.objects.filter(id=user_id).update(Name=user_name,completename=complete_username,Email=useremail,
                            PhoneNo=phoneno,Gender=gender,DateOfBirth=dob,User_Type=usertype,City=usercity,Country=usercountry,
                            AboutMe=useraboutme)
    
        messages.warning(request, "Sucessfully Updated!")
    
        return render(request, 'edit.html',{'q':q})
        
        
        
        
       else:
        
        return render(request, 'edit.html',{'q':q,'data':data})
     elif q == "2" :
      if request.POST:
       
        educationtype=request.POST['educationtype']
        currentuni=request.POST['currentuni']
        current_edu_from=request.POST['current_edu_from']
        current_edu_to=request.POST['current_edu_to']
        edu_city=request.POST['edu_city']
        edu_country=request.POST['edu_country']
        
        
        obj = Demo.objects.filter(id=user_id).update(Education_type=educationtype,Current_Education_Place=currentuni,
                           Current_Education_Date_From=current_edu_from,Current_Education_Date_To=current_edu_to,
                           Current_Education_City=edu_city,Current_Education_Country=edu_country)
    
        messages.warning(request, "Sucessfully Updated!")
    
        return render(request, 'edit.html',{'q':q})
        
      else:
            return render(request, 'edit.html',{'q':q,'data':data})
     elif q == "3" :
      
      if request.POST:
                
        user_interest=request.POST['user_interest']
        
        
        obj = Demo.objects.filter(id=user_id).update(Interest=user_interest)
    
        messages.warning(request, "Sucessfully Updated!")
    
        return render(request, 'edit.html',{'q':q})
      else:
         return render(request, 'edit.html',{'q':q,'data':data})
 else:
         return redirect('login')
