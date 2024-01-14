from django.shortcuts import render

def home(request):
    data={'title': 'Control CNC'}
    return render(request, 'marlin_web_control.html', context=data)
