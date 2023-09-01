from cgitb import lookup
import django_filters
from django_filters import rest_framework as filters
from django_filters import DateFilter, CharFilter
from .models import *


class EmployeeFilter(django_filters.FilterSet) :
    
    class Meta:
        model = Employee
        fields = ["name", "eid"]