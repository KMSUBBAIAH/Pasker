from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from password_locker.helper import fernet_encrypt_data, fernet_decrypt_data
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class EmployeeDataSecurity(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    private_key = models.BinaryField()
    public_key = models.BinaryField()


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Employee, through='TeamMembership')
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    has_authority = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name


class ProtectedData(models.Model):
    service_name = models.CharField(max_length=100)
    service_username = models.BinaryField(editable=True)
    service_password = models.BinaryField(editable=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.service_name} - {self.created_by.username}'
    
    def get_absolute_url(self):
        return reverse('credential-detail', kwargs={'pk': self.pk})
    

    





