from django.contrib import admin
from .models import CustomUser, Parent, Child

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent')
