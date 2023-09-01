from time import strftime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from vacaapp.filters import EmployeeFilter
from .models import Attendance, Vacation, Employee
from .forms import VacationForm, AttendanceForm, EmployeeADD
# from vacapp.management.commands import rd_update
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, timedelta 
from django.shortcuts import get_object_or_404, redirect
import datetime
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.views.generic import ListView
from django.db.models import Q
from django.db.models.functions import ExtractMonth
from django.urls import reverse
from django.utils.text import slugify




def Home(request):
    employee = Employee.objects.all()
    context ={
        'employee' :employee,
    }
    return render (request,'home.html',context)
    

@login_required
def user_view(request):

    employee = Employee.objects.all()
    employee_count = Employee.objects.all().count()
    me = request.user.id
    user_employees = Employee.objects.filter(user = me )
    filter = EmployeeFilter(request.GET, queryset=Employee.objects.all().order_by("eid")) 
    employee = filter.qs
   

    context={

       'filter':filter,
        'employee':employee,
        'employee_count':employee_count,
        'user_employees':user_employees,
      
    

    }
    return render(request,'userview.html', context)  

@login_required
def employeeaddform(request):
    if request.method == "POST":
        form = EmployeeADD(request.POST)   
        form.is_valid()
        form.instance.name = form.cleaned_data['name']
        form.instance.eid = form.cleaned_data["eid"] 
        form.instance.title = form.cleaned_data['title']
        form.instance.yearly_balance = form.cleaned_data['yearly_balance']
        
        form.instance.save()
        print(form.instance,"//////////////////////////////////////////////////////////////////////////////////////////////////////")
        messages.success(request, 'The Employee has been added Successfully.')
        return HttpResponseRedirect("/") 
    else:
        form = EmployeeADD()
    context = {
        'form':form,

    } 
    return render (request,'addemployee.html',context)                 




@login_required
def get_employee(request,id):
    one_employee =  get_object_or_404(Employee,id=id )
    vacation = Vacation.objects.all().order_by('st_date')
    attendance = Attendance.objects.all()
    employee = Employee.objects.all()
    me = request.user.id
    users = Employee.objects.filter(user=me)
    ah_leaves_balance = Vacation.objects.filter(vacation_type="AH",user__id=id).order_by('st_date')
    ahe_leaves_balance = Vacation.objects.filter(vacation_type="AHE",user__id=id).order_by('st_date')
    leaves = Vacation.objects.filter(vacation_type="RD",user__id=id).order_by('st_date')
    rdes   = Attendance.objects.filter(active=True,user__id=id).order_by('date')
    rdes_count = sum(rdes.values_list("count_of_days",flat=True))
    ah_count   = sum(ah_leaves_balance.values_list("day_count",flat=True))
    ahe_count  = sum(ahe_leaves_balance.values_list("day_count",flat=True))
    remaining_balance = (one_employee.yearly_balance + one_employee.resdual_vacations) - (ah_count + ahe_count)
    vacation1 = Vacation.objects.filter(vacation_type="RD",user__id=id).count()
    vacation2 = Vacation.objects.filter(vacation_type="AH",user__id=id).count()
    vacation3 = Vacation.objects.filter(vacation_type="AHE",user__id=id).count()
    Vacation4 = Vacation.objects.filter(st_date__month = 4, user__id = id)
    taken=[]
    taken_attendance_day = Attendance.objects.filter(active = False , user__id = id)
    for v in Vacation4 :
        if v.st_date.month == 4:
            one_employee.resdual_vacations = 0
            remaining_balance = one_employee.yearly_balance - (ah_count + ahe_count)

    for l in leaves :
            
            lvrd = l.vrd
            lstartdate = l.st_date
            for r in rdes :
                
                rdate = r.date
                status = r.active
                if lvrd == rdate:
                    r.count_of_days -= 1
                    rdes_count -= 1 
                if r.count_of_days <= 0:

                    r.active = False
                 
    true_attendance = Attendance.objects.filter(active = True , user__id = id )    
    for s in taken_attendance_day:
        sdate = s.date
        european_format = "%d-%m-%Y"
        taken.append(sdate)
       

    
       
    context ={
                   
                    "one_employee":one_employee,
                    "employee":employee,
                    'vacation':vacation,
                    'leaves':leaves,
                    'rdes':rdes,
                    "rdes_count":rdes_count,
                     "taken":taken,
           'users':users,
                    'attendance':attendance,
                    'remaining_balance': remaining_balance,
                    'vacation1':vacation1,
        'vacation2':vacation2,
        'vacation3':vacation3,
        'Vacation4':Vacation4,
        'true_attendance':true_attendance,
        'ah_count':ah_count,
        'ahe_count':ahe_count,
        

                  
    }
    return render(request,"one_employee.html ",context)


@login_required
def employee_edit(request, id):                                         
    data = get_object_or_404(Employee, id=id)
    form = EmployeeADD(instance=data)                                                               

    if request.method == "POST":
        form = EmployeeADD(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect ('/')
    context = {
        "form":form
    }
    return render(request, 'employee_update.html', context)


@login_required
def vacation_edit(request, id):                                         
    data = get_object_or_404(Vacation, id=id)
    form = VacationForm(instance=data)                                                               

    if request.method == "POST":
        form = VacationForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect ('/')
    context = {
        "form":form
    }
    return render(request, 'vacation_update.html', context)


@login_required
def attendance_edit(request, id):                                         
    data = get_object_or_404(Attendance, id=id)
    form = AttendanceForm(instance=data)                                                               

    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect ('/')
    context = {
        "form":form
    }
    return render(request, 'attendane_update.html', context)


@login_required
def vacationadd(request, id):
    if request.method == 'POST':
        form = VacationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Create a new Vacation instance with the cleaned data
            vacation = Vacation(
                user=data['user'],
                st_date=data['st_date'],
                end_date=data['end_date'],
                day_count=data['day_count'],
                vrd=data['vrd'],
                vacation_type=data['vacation_type'],
                comments=data['comments']
            )

            try:
                # Call the clean() method to perform validation and cleaning
                vacation.clean()

                # Call the save() method to save the new Vacation instance
                vacation.save()
                messages.success(request, 'Your Vacation has been added Successfully.')
                return HttpResponseRedirect("/")
            except ValidationError as e:
                # Handle any validation errors that may occur
                messages.error(request, str(e))
        else:
            messages.error(request, 'Invalid data entered')
    else:
        form = VacationForm()

    context = {
        'form': form,
    }
    return render(request, 'vacation_add.html', context)  



@login_required
def attendanceadd(request,id):

    attendance = Attendance.objects.all()
    vacation = Vacation.objects.all()
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        form.is_valid()
        form.instance.user = form.cleaned_data['user']
        form.instance.date = form.cleaned_data['date']
        form.instance.day_name = form.cleaned_data['day_name']
        form.instance.count_of_days = form.cleaned_data['count_of_days']
        form.instance.active = form.cleaned_data['active']
        form.instance.original_balance = form.cleaned_data['original_balance']
        
        form.instance.save()
        print(form.cleaned_data,'Formmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
        messages.success(request, 'Your Attendance has been added Successfully.')
        
        
        
                       
        return HttpResponseRedirect("/") 
    else:
            form = AttendanceForm()
    context= {

        'form':form,
    }
    return render(request, 'attendanceadd.html', context)     


class VacationByMonthView(ListView):
    model = Vacation
    template_name = "vacation_by_month.html"
    context_object_name = "vacations"
    paginate_by = 10

    def get_queryset(self):
        month_name = self.kwargs.get("month_name")
        month_number = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}.get(month_name.lower())
        queryset = super().get_queryset().filter(st_date__month=month_number)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(user__username__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        month_name = self.kwargs.get("month_name", today.strftime("%B"))
        context["month_name"] = month_name
        context["search_query"] = self.request.GET.get("search")
        return context
    
    
def choose_month(request):
    if request.method == "POST":
        month_name = request.POST.get("month")
        return redirect(reverse("vacations_by_month", kwargs={"month_name": slugify(month_name)}) + f"?next={reverse('userview')}")
    else:
        return render(request, "choose_month.html")        
    
    
def issue_due_date(request):
    data = [
        {'id': 1, 'name': '360 Extruder cylinder', 'due_date': datetime(2023, 5, 3)},
        {'id': 2, 'name': 'mandrel cooling valve 360LV', 'due_date': datetime(2023, 5, 15)},
        {'id': 3, 'name': 'purachase 460SV vacuum pump Heat Exchanger', 'due_date': datetime(2023, 5, 30)},
        {'id': 4, 'name': 'maintain 312SV mandrell unit', 'due_date': datetime(2023, 5, 20)},
        {'id': 5, 'name': 'refix the Bm6 mould (1000ml)', 'due_date': datetime(2023, 5, 2)},
    ]

    # Check if a new issue was submitted
    if request.method == 'POST':
        id_str = request.POST.get('id')
        if id_str:
            id = int(id_str)
        else:
            id = None
        name = request.POST.get('name')
        due_date_str = request.POST.get('due_date')
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        else:
            due_date = None
        for item in data:
            if item['id'] == id:
                item['name'] = name
                item['due_date'] = due_date
                break
        else:
            # If no item was found with the given id, create a new item
            new_item = {'id': id, 'name': name, 'due_date': due_date}
            data.append(new_item)
        

    today = datetime.today()
    for item in data:
        if item['due_date'] is None:
            item['message'] = ''
        elif item['due_date'] < today:
            # Delete the item if it is overdue
            data.remove(item)
        elif item['due_date'] < today + timedelta(days=3):
            item['message'] = 'You still have three days until your issue is due for execution.'
        else:
            item['message'] = ''

    # Convert the datetime objects to strings
    for item in data:
        if item['due_date'] is not None:
            item['due_date'] = item['due_date'].strftime('%Y-%m-%d')

    return render(request, 'issue_due_date.html', {'data': data})
