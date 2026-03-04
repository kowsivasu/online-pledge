from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class Pledge(models.Model):

    name = models.CharField(max_length=100)
    pledge_text = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    # new fields
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=300, blank=True)
    emp_code = models.CharField(max_length=500, blank=True)
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=300, blank=True)
    place = models.CharField(max_length=300, blank=True)
    pledgeLanguage = models.CharField(max_length=2,
                                choices=[
                                    ('TA', 'Tamil'),
                                    ('EN', 'English'),
                                    ('HI', 'Hindi'),],
                                    default='EN'
                                    )
    pledgeName = RichTextField(null=True, blank=True)
        
    def __str__(self):
        return self.name
    
class Admin(models.Model):
    adminName = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    mobile = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adminName

class pledgeCreate(models.Model):
    pledgeName = RichTextField()
    logo1 = models.ImageField(upload_to='logos/', blank=True)
    logo2 = models.ImageField(upload_to='logos/', blank=True)
    logo3 = models.ImageField(upload_to='logos/', blank=True)
    pledgeText = RichTextField()
    checkboxText = models.CharField(max_length=2000, blank=True)
    tamilPledgeText = RichTextField(null=True, blank=True)
    hindiPledgeText = RichTextField(null=True, blank=True)
    tamilPledgeName = RichTextField(null=True, blank=True)
    hindiPledgeName = RichTextField(null=True, blank=True)

    
    