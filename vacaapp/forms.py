from dataclasses import field, fields
import datetime
from django import forms
from .models import  Vacation, Attendance, Employee

from django.contrib.auth.models import User







VACATION_CHOICES=(
    ('AH','AH'),
    ('AHE','AHE'),
    ('RD','RD'),
    )
class VacationForm(forms.ModelForm):    
    st_date = forms.DateField(required = True ,widget=forms.DateInput(attrs={'type': 'date'}))
    end_date   =   forms.DateField(required = True ,widget=forms.DateInput(attrs={'type': 'date'})) 
    vrd = forms.DateField(required = False ,widget=forms.DateInput(attrs={'type': 'date'}))
    
    vacation_type  = forms.ChoiceField(
        widget=forms.RadioSelect, choices=VACATION_CHOICES)
     
    class Meta():
        model = Vacation
        fields = "__all__"
        
        
        widgets = {
            "day_count": forms.NumberInput(attrs={
                "class": "form-control","id":"day_count",
                "placeholder": "vacation days count.",
                
            }),

           
            
        }




class AttendanceForm(forms.ModelForm):
    date = forms.DateField(required = True ,widget=forms.DateInput(attrs={'type': 'date'}))
    day_name = forms.DateField(required = True ,widget=forms.DateInput(attrs={'type': 'date'}))
    # taken = forms.DateField(required = False ,widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta():
        model = Attendance
        fields = "__all__"    
        widgets = {
            "count_of_days": forms.NumberInput(attrs={
                "class": "form-control","id":"count_of_days",
                "placeholder": "RD days count.",
                
            }),
            
             "comments": forms.TextInput(attrs={
                "class": "form-control text-center",
                "placeholder": "Your comments here.",
            }),

           
            
        }   
   




class EmployeeADD(forms.ModelForm):
    class Meta():
        model = Employee
        fields = "__all__"



class FilterForm(forms.ModelForm):
    
    
    class Meta():
        model = Employee
        fields = ["name","eid"]


