from django.contrib import admin
from .models import Account,AnimalForm,Blacklist,Help
from import_export.admin import ImportExportModelAdmin  
from import_export import resources
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )
    
class AnimalFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'email', 'animal_name')
    
admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Account)
admin.site.register(AnimalForm, AnimalFormAdmin)
admin.site.register(Blacklist)
admin.site.register(Help)
