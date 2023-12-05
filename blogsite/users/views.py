from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForms, UserUpdateForms, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

from .send_rfid import get_auth_id
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Authentication
from .decorators import (
    is_authorized
)
from .tokens import account_activation_token

from password_locker.models import (Employee, Team, Role, 
                                    TeamMembership, EmployeeDataSecurity,)
import json
from password_locker.helper import *
from password_locker.utils import *
# from .forms import SignUpForm

UserModel = get_user_model()

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("users/acc_active_email.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForms(request.POST)
        # form = AuthUserRegisterForms(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            auth_id = form.cleaned_data['authentication_id']
            # Dispatch the custom registration signal with the authentication ID
            Authentication.objects.create(user=user, authentication_id=auth_id)
            
            #Password Locker Models Save
            team_name = form.cleaned_data['team']
            role_name = form.cleaned_data['role']
            has_authority = (role_name == 'TeamLead')

            employee = Employee.objects.create(user=user)
            team, created = Team.objects.get_or_create(name=team_name)
            role, created = Role.objects.get_or_create(name=role_name, has_authority=has_authority)
            TeamMembership.objects.create(employee=employee, team=team, role=role)
            
            if employee:
                # Data Security
                # private_key = Fernet.generate_key()
                # public_key = Fernet.generate_key()
                private_key,public_key = generate_keys()
                public_key = serialize_public_key(public_key)
                private_key = serialize_private_key(private_key)
                # Set the keys in the model and save
                EmployeeDataSecurity.objects.create(employee=employee, 
                                                    private_key = private_key,
                                                    public_key = public_key)
        
            activateEmail(request, user, form.cleaned_data.get('email'))
            # messages.success(request,f'Account has been created! You can now login!')   
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegisterForms()
    context = {'form': form, 'role_choices': json.dumps(form.role_choices)}
    # print(form.role_choices)
    return render(request,'users/register.html',context)


from django.shortcuts import render
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = 'users/authentication.html'  # Specify the URL for the custom template

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    def dispatch(self, request, *args, **kwargs):
        # Your custom logic before logging out the user
        # For example, updating the is_authorized attribute
        authentication = request.user.authentication
        authentication.is_authorized = False
        authentication.save()

        # Call the parent class's dispatch method to perform the actual logout
        return super().dispatch(request, *args, **kwargs)
    

@login_required
def authentication(request):
    # get_auth_id()
    if request.method == 'POST':
        # entered_code = request.POST.get('authentication_id')
        # while True:
            entered_code = get_auth_id().strip()
            # print(entered_code)
            user = request.user
            user_auth = user.authentication
            if entered_code == user_auth.authentication_id:
                user_auth.is_authorized = True
                user_auth.save()
                return redirect('blog-home')
            elif entered_code != user_auth.authentication_id:
                return render(request, 'users/authentication.html', {'error': 'Invalid code'})
    return render(request, 'users/authentication.html')


# @login_required
@is_authorized
def profile(request):
    if request.method =='POST':
        u_form = UserUpdateForms(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES ,instance=request.user.profile)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"{request.user.username}'s account has been updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForms(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'users/profile.html',context)


from django.http import JsonResponse
def get_csrf_token(request):
    return JsonResponse({'csrf_token': request.COOKIES.get('csrftoken', '')})
