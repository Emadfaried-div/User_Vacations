from django.urls import path
from django.conf.urls.static import static
from . import views



urlpatterns=[
    path('',views.Home, name="home"),
    path('user_view/',views.user_view,name = 'userview'),
    path('employeeaddform/',views.employeeaddform, name='employeeaddform'),
    path('vacation_add/<int:id>/',views.vacationadd,name='vacationadd'),
    path('get_employee/<int:id>/',views.get_employee, name='one_employee'),
    path('attendance_add/<int:id>/',views.attendanceadd , name='attendanceadd'),
    path('employee_edit/<int:id>/',views.employee_edit, name= "employee_edit"),
    path('vacation_edit/<int:id>/',views.vacation_edit, name= "vacation_edit"),
    path('attendance_edit/<int:id>/',views.attendance_edit, name= "attendance_edit"),
    path("vacations/month/<str:month_name>/", views.VacationByMonthView.as_view(), name="vacations_by_month"),
    path("vacations/choose_month/", views.choose_month, name="choose_month"),
    path("issue_due_date/",views.issue_due_date, name="issue_due_date"),
    
    
    
]