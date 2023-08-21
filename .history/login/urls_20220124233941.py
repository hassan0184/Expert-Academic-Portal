from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('login', views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('newRegestrations', views.newRegestrations,name='newRegestrations'),
    path('logout', views.logout,name='logout'),
    path('new_query', views.new_query,name='new_query'),
    path('readmore', views.readmore,name='readmore'),
    path('search_post', views.search_post,name='search_post'),
    path('delete_post', views.delete_post,name='delete_post'),
    path('raised_post_delete', views.raised_post_delete,name='raised_post_delete'),
    path('approved_post', views.approved_post,name='approved_post'),
    path('delete_comment', views.delete_comment,name='delete_comment'),
    path('update_post/<int:id>', views.update_post,name='update_post'),
    path('updated_query', views.updated_query,name='updated_query'),
    path('update_comment', views.update_comment,name='update_comment'),
    path('reply_comment', views.reply_comment,name='reply_comment'),
    path('forgetpassword', views.forgetpassword,name='forgetpassword'),
    path('changepassword', views.changepassword,name='changepassword'),
    path('changepassword', views.changepassword,name='changepassword'),
    path('timeline', views.timeline,name='timeline'),
    path('userimage/<int:id>', views.userimage,name='userimage'),
    path('dislike', views.dislike,name='dislike'),
    path('like', views.like,name='like'),
    path('follow', views.follow,name='follow'),
    path('adminprofile', views.adminprofile,name='adminprofile'),
    path('edit-profile', views.edit,name='edit'),
    
    
    
]

