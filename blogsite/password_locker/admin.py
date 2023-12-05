from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(Role)
admin.site.register(TeamMembership)
admin.site.register(ProtectedData)
admin.site.register(EmployeeDataSecurity)
# admin.site.register(DataAccessPermission)