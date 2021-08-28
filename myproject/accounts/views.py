from django.shortcuts import render


def logged(request):
    template_name = 'accounts/logged.html'
    return render(request, template_name)
