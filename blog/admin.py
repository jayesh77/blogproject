from django.contrib import admin

# Register your models here.
from blog.models import Profile, Post

admin.site.register(Profile)
admin.site.register(Post)
