from django import forms
from .models import Pledge, Admin, pledgeCreate
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class PledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = [
            'name',
            'email',
            'department',
            'designation',
            'emp_code',
            'state',
            'city',
            'district',
            'place',
            'pledgeLanguage',

        ]
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'required': True}),
            'department': forms.TextInput(attrs={'id': 'department','required': True}),
            'designation': forms.TextInput(attrs={'id': 'designation','required': True}),
            'emp_code': forms.TextInput(attrs={'id': 'emp_code','required': True}),
            'state': forms.TextInput(attrs={'id': 'state','required': True}),
            'city': forms.TextInput(attrs={'id': 'city','required': True}),
            'district': forms.TextInput(attrs={'id': 'district','required': True}),
            'place': forms.TextInput(attrs={'id': 'place','required': True}),
            'pledgeLanguage': forms.Select(attrs={'id': 'pledgeLanguage','required': True}),
        }
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']       
        
class PledgeCreateForm(forms.ModelForm):
    class Meta:
        model = pledgeCreate
        fields = ['pledgeName', 'logo1', 'logo2', 'logo3', 'pledgeText', 'checkboxText', 'tamilPledgeText', 'hindiPledgeText']
        widgets = {
            # 'pledgeName': CKEditorWidget(config_name='default'),
            'logo1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'logo2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'logo3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pledgeText': forms.Textarea(attrs={'class': 'form-control'}),
            'checkboxText':forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 50px;'}),
            'tamilPledgeText': forms.Textarea(attrs={'class': 'form-control'}),
            'hindiPledgeText': forms.Textarea(attrs={'class': 'form-control'}),

        }