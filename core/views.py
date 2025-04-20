from django.shortcuts import redirect

def redirect_to_oidc(request):
    return redirect('/oidc/authenticate/')
