from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'service_rattachement', 'is_staff')
    list_filter = ('role', 'service_rattachement', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations MedObs', {'fields': ('role', 'service_rattachement')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations MedObs', {'fields': ('role', 'service_rattachement')}),
    )