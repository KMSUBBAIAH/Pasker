from django.shortcuts import redirect
from django.urls import reverse

def is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            user_auth = user.authentication 
            entered_code = request.POST.get('authentication_id')

            if user_auth.authentication_id == entered_code:
                user_auth.is_authorized = True
                user_auth.save()

            if user_auth.is_authorized:
                return view_func(request, *args, **kwargs)
            
        return redirect(reverse('authentication'))
    return wrapper
