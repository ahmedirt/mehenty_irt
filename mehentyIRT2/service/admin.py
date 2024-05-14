from django.contrib import admin
from .models import Customer,Technician,Request,Attendance,Feedback
# Register your models here.
# admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Technician)
admin.site.register(Request)
admin.site.register(Attendance)
admin.site.register(Feedback)