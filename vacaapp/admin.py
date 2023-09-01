from django.contrib import admin
from .models import *
from django import forms
from . import views



from django.contrib.admin import AdminSite
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from django.http import HttpResponse
# Register your models here.




class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'title', 'eid','yearly_balance')
    list_filter = ('eid', 'title')
    search_fields = ('user__username', 'eid')
    ordering = ('eid',)
    
admin.site.register(Employee, EmployeeAdmin)


class VacationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'st_date', 'end_date', 'day_count', 'vrd', 'vacation_type', 'comments')
    list_filter = ('vacation_type',)
    search_fields = ('user__username',)
    ordering = ('-st_date',)
    readonly_fields = ('day_count',)
    
admin.site.register(Vacation, VacationAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        forms.CharField: {'widget': forms.TextInput(attrs={'class': 'vTextField text-center'})},
        forms.DateField: {'widget': forms.DateInput(attrs={'class': 'vDateField text-center'})},
        forms.TimeField: {'widget': forms.TimeInput(attrs={'class': 'vTimeField text-center'})},
        forms.DateTimeField: {'widget': forms.DateTimeInput(attrs={'class': 'vDateTimeField text-center'})},
        forms.IntegerField: {'widget': forms.NumberInput(attrs={'class': 'vIntegerField text-center'})},
        forms.FloatField: {'widget': forms.NumberInput(attrs={'class': 'vDecimalField text-center'})},
    }
    list_display = ('user', 'date', 'day_name', 'count_of_days', 'active', 'original_balance', 'comments')
    list_filter = ('user', 'active')
    search_fields = ('user__username', 'date')
    ordering = ('-date',)

admin.site.register(Attendance, AttendanceAdmin)


   