from django.contrib import admin

from .models import Care, Advice, Category, Pictures, Post, CustomUser

# Register your models here.
admin.site.register(Care)
admin.site.register(Advice)
admin.site.register(Category)
admin.site.register(Pictures)
admin.site.register(Post)
admin.site.register(CustomUser)