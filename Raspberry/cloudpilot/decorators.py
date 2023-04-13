from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    # czyli tu mamy jeszcze dodatkowy poziom opakowania, ponieważ dekorator otrzymuje argumenty
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                group = request.user.groups.all()
                user_group_names=[]
                for x in group:
                    if x.name in allowed_roles:
                        return view_func(request, *args, **kwargs)

            return HttpResponse('Nie masz dostępu do tej strony')
                
        return wrapper_func
    return decorator