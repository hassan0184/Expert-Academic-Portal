from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Demo)
admin.site.register(Query)
admin.site.register(Comment)
admin.site.register(RaisedQuery)
admin.site.register(Followers)
admin.site.register(CheckReaction)
admin.site.register(Notification)
admin.site.register(TrendsTopic)