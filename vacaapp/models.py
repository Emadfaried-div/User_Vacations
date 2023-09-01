from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.



VACATION_CHOICES=(
    ('AH','AH'),
    ('AHE','AHE'),
    ('RD','RD'),
    )

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)
    eid = models.PositiveIntegerField()
    title = models.CharField(max_length=100,blank=True,null=True)
    yearly_balance = models.PositiveIntegerField()
    resdual_vacations =  models.PositiveIntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return str(self.name)




class Attendance(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date = models.DateField(blank=True,null=True)
    day_name = models.DateField(blank=True,null=True)
    count_of_days = models.PositiveIntegerField(blank=True,null=True,default ='1')
    active = models.BooleanField(blank=True , null= True , default= True )
    
    original_balance = models.CharField(max_length=20,blank=True, null=True)
    comments = models.CharField(max_length=250,blank=True,null=True)
    
    
    def __str__(self):
        return f'{self.user.username} / {self.date}'
    


class Vacation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    st_date  = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    day_count = models.PositiveIntegerField(blank=True,null=True,default='1')
    vrd      = models.DateField(blank=True,null=True)
    vacation_type = models.CharField(max_length=50,choices=VACATION_CHOICES,blank=True,null=True)
    comments = models.CharField(max_length=250,blank=True,null=True)
    
    def clean(self):
        if self.st_date > self.end_date:
            raise ValidationError(_('Start date cannot be after end date.'))
        
        
        if self.vrd and self.vrd > self.st_date:  # Add a check for None
            raise ValidationError(_('RD_date cannot be after Start_date.'))
        
        
         # Custom validation for RD vacation type and count_of_days
        # if self.vacation_type == 'RD':
        #     attendance = Attendance.objects.filter(user=self.user, date=self.vrd, count_of_days=0)
        #     if not attendance.exists():
        #         raise ValidationError(_('We are sorry, but the RD date you have selected has zero available days. Please choose another RD date.'))
        
    def __str__(self):
        return  f'{self.id}/{self.user.username} / {self.st_date}'