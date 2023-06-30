from django.shortcuts import render

def home(request):
    data={'title': 'Control CNC'}
    return render(request, 'fluidnc_control.html', context=data)
