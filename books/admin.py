from django.contrib import admin
from .models import Book, MyBook

# Register your models here.
admin.site.register(Book)
admin.site.register(MyBook)