from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from .models import ProtectedData
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from users.decorators import (is_authorized)
from django.urls import reverse_lazy
from .models import ProtectedData, EmployeeDataSecurity, Employee, Team
from password_locker.forms import PasswordLockerForm, PasswordLockerUpdateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Fernet Encryption
from password_locker.helper import *
# RSA Encryption
from password_locker.utils import *


@method_decorator(is_authorized, name='dispatch')
class CredentialListView(ListView):
    model = ProtectedData
    # context_object_name = 'protected_data_list'
    template_name = 'password_locker/credentials.html' 
    # paginate_by = 6
    def process_team_data(team_data):
        return sorted(team_data, key=lambda x: x.service_name)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.GET.get('search')
        if search_param:
            queryset = queryset.filter(service_name__icontains=search_param)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        # paginated_queryset = context['object_list']
        # Add the paginated_queryset to the context
        # context['protected_data_list'] = paginated_queryset
        if self.get_queryset() is None:
            context['protected_data_list'] = ProtectedData.objects.all()
        context['protected_data_list'] = self.get_queryset()
        return context
    
@is_authorized
def create_credential(request):
    if request.method =='POST':
        p_form = PasswordLockerForm(request.POST, instance=request.user)
        if 'generate-password' in request.POST:
            generated_password = generate_secure_password()
            # Update the form data with the generated password
            p_form.data = p_form.data.copy()
            p_form.data['service_password'] = generated_password

        if p_form.is_valid():
            logged_emp = Employee.objects.get(user=request.user)
            eds = EmployeeDataSecurity.objects.get(employee=logged_emp)
            service = p_form.cleaned_data.get('service_name')
            username = p_form.cleaned_data.get('service_username')
            password = p_form.cleaned_data.get('service_password')
            if not password:
                password = generated_password
                # p_form.cleaned_data['service_password'] = password
            # # Fernet Encyption
            # secret_key = eds.private_key
            # username = fernet_encrypt_data(secret_key, username)
            # password = fernet_encrypt_data(secret_key, password)
            # RSA Encryption
            public_key = deserialize_public_key(eds.public_key)
            username = rsa_encrypt_data(username, public_key)
            password = rsa_encrypt_data(password, public_key)
            ProtectedData.objects.create(service_name=service, service_username=username,
                                         service_password=password, created_by=request.user)
            return redirect('credentials_view')
        
    else: p_form = PasswordLockerForm(instance=request.user) 

    context = {'p_form' : p_form,}
    context['teams'] = Team.objects.all()
    context['protected_data_list'] = ProtectedData.objects.all()
    return render(request,'password_locker/protecteddata_form.html',context)

    
@is_authorized
def detail_credential(request, pk):
    protected_data = get_object_or_404(ProtectedData, pk=pk)
    created_by_emp = Employee.objects.get(user=protected_data.created_by)
    eds = EmployeeDataSecurity.objects.get(employee=created_by_emp)
    service = protected_data.service_name
    username = protected_data.service_username
    password = protected_data.service_password
    # # Fernet Encryption
    # secret_key = eds.private_key
    # username = fernet_decrypt_data(secret_key, username)
    # password = fernet_decrypt_data(secret_key, password)
    # RSA Encryption
    private_key = deserialize_private_key(eds.private_key)
    username = rsa_decrypt_data(username, private_key)
    password = rsa_decrypt_data(password, private_key)
    object={
        'service_name':service,
        'service_username':username,
        'service_password':password,
        'created_by':created_by_emp.user,
        'id':pk
    }
    context = {'object':object}
    context['teams'] = Team.objects.all()
    context['protected_data_list'] = ProtectedData.objects.all()
    return render(request,'password_locker/protecteddata_detail.html',context)

@is_authorized
def update_credential(request, pk):
    protected_data = get_object_or_404(ProtectedData, pk=pk)
    logged_emp = Employee.objects.get(user=request.user)
    eds = EmployeeDataSecurity.objects.get(employee=logged_emp)
    private_key = deserialize_private_key(eds.private_key)

    if request.method =='POST':
        p_form = PasswordLockerForm(request.POST, instance=request.user)
        if p_form.is_valid():
            logged_emp = Employee.objects.get(user=request.user)
            eds = EmployeeDataSecurity.objects.get(employee=logged_emp)
            protected_data.service_name = p_form.cleaned_data.get('service_name')
            username = p_form.cleaned_data.get('service_username')
            password = p_form.cleaned_data.get('service_password')
            # # Fernet Encryption
            # secret_key = eds.private_key
            # protected_data.service_username = fernet_encrypt_data(secret_key, username)
            # protected_data.service_password = fernet_encrypt_data(secret_key, password)
            # RSA Encryption
            public_key = deserialize_public_key(eds.public_key)
            protected_data.service_username = rsa_encrypt_data(username, public_key)
            protected_data.service_password = rsa_encrypt_data(password, public_key)
            protected_data.save()
            return redirect('credentials_view')
    else:
        initial_data = {
            'service_name': protected_data.service_name,
            'service_username': rsa_decrypt_data(protected_data.service_username, private_key),
            'service_password': rsa_decrypt_data(protected_data.service_password, private_key),
        }
        p_form = PasswordLockerForm(instance=protected_data, initial=initial_data)

    context = {
        'p_form': p_form,
        'is_update': True,
        'object': {
            'service_name': protected_data.service_name,
            'service_username': rsa_decrypt_data(protected_data.service_username, private_key),
            'service_password': rsa_decrypt_data(protected_data.service_password, private_key),
            'created_by': protected_data.created_by,
            'id': pk,
        },
        'teams': Team.objects.all(),
        'protected_data_list': ProtectedData.objects.all(),
    }
    return render(request, 'password_locker/protecteddata_form.html', context)


@is_authorized
def delete_credential(request, pk):
    protected_data = get_object_or_404(ProtectedData, pk=pk)
    logged_emp = Employee.objects.get(user=request.user)
    eds = EmployeeDataSecurity.objects.get(employee=logged_emp)
    private_key = deserialize_private_key(eds.private_key)

    if request.method == 'POST':
        protected_data.delete()
        return redirect('credentials_view')
    initial_data = {
        'service_name': protected_data.service_name,
        'service_username': rsa_decrypt_data(protected_data.service_username, private_key),
        'service_password': rsa_decrypt_data(protected_data.service_password, private_key),
    }
    p_form = PasswordLockerForm(initial=initial_data)
    context = {
        'p_form': p_form,
        'is_update': True,
        'object': {
            'service_name': protected_data.service_name,
            'service_username': rsa_decrypt_data(protected_data.service_username, private_key),
            'service_password': rsa_decrypt_data(protected_data.service_password, private_key),
            'created_by': protected_data.created_by,
            'id': pk,
        },
        'teams': Team.objects.all(),
        'protected_data_list': ProtectedData.objects.all(),
    }
    return render(request, 'password_locker/protecteddata_confirm_delete.html', context)
