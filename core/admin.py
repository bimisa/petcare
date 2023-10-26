from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Appointment, Company, Vaccination, Pet


User = get_user_model()

class CustomUserAdmin(UserAdmin):
    # model = CustomUser
    list_display = ['username', 'email', 'role']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'service_provider')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Pet)
admin.site.register(Vaccination)
admin.site.register(Appointment)
admin.site.register(Company)
