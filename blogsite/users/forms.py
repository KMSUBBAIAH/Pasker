from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Profile
# from .models import CustomUser

class UserRegisterForms(UserCreationForm):
    email = forms.EmailField(required=True)
    authentication_id = forms.CharField(max_length=9,required=True)
    team_choices = [
        ('Development', 'Development Team'),
        ('QualityAssurance', 'Quality Assurance Team'),
        ('DevOps', 'DevOps Team'),
        ('ProductManagement', 'Product Management Team'),
    ]

    role_choices = {
        'Development': [
            ('SoftwareEngineer', 'Software Engineer'),
            ('SeniorSoftwareEngineer', 'Senior Software Engineer'),
            ('TeamLead', 'Team Lead'),
            ('SoftwareArchitect', 'Software Architect'),
        ],
        'QualityAssurance': [
            ('QAEngineer', 'QA Engineer'),
            ('SeniorQAEngineer', 'Senior QA Engineer'),
            ('QALead', 'QA Lead'),
            ('TestAutomationEngineer', 'Test Automation Engineer'),
        ],
        'DevOps':[
            ('DevOpsEngineer', 'DevOps Engineer'),
            ('ReleaseEngineer', 'Release Engineer'),
            ('SystemAdministrator', 'System Administrator'),
            ('CloudArchitect', 'Cloud Architect'),
        ],
        'ProductManagement':[
            ('ProductManager', 'Product Manager'),
            ('AssociateProductManager', 'Associate Product Manager'),
            ('ProductOwner', 'Product Owner'),
            ('ProductCoordinator','Product Coordinator')
        ],
    }

    team = forms.ChoiceField(choices=team_choices,required=True)
    role = forms.ChoiceField(choices=role_choices['Development'], required=False)
    # Set initial role choices for 'development' team

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = self.role_choices.get(self.initial.get('team', 'Development'), [])

    def clean_team(self):
        team = self.cleaned_data.get('team', 'Development')
        self.fields['role'].choices = self.role_choices.get(team, [])
        return team

    class Meta:
        model = User
        fields = ['username','email','password1','password2','authentication_id','team','role']


class UserUpdateForms(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# class AuthUserRegisterForms(UserCreationForm):
#     authentication_id = forms.CharField(max_length=10, required=True)
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2', 'authentication_id')
