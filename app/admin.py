from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from app.models import *


admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Comment)