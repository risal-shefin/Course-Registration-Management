from django.contrib import admin
from .models import Form
from .models import Counter

# Register your models here.
admin.site.register(Form)
admin.site.register(Counter)