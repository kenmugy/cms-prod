from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request,*args, **kwargs)
    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator_func(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponse('Your not Authorised to view this page')
        return wrapper_func
    return decorator_func          
        
        
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'shop':
            return redirect('user')
        elif group == 'store':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper_func
        
    