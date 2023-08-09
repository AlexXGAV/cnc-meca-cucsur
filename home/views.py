from django.shortcuts import render, redirect
from cnc_meca_cucsur.settings import EMAIL_HOST_USER
from .forms import ContactForm
from django.core.mail import EmailMessage
from .models import Teammate, Gallery
from django.utils.translation import gettext_lazy as _

def home(request):
    contact_form = ContactForm()
    team = Teammate.objects.all()
    galleries = Gallery.objects.all()
    gallery_data = [(gallery, _(str(gallery.get_gallery_display()))) for gallery in galleries]

    if request.method == "POST":
        print("Hola")
        formulario_contacto = ContactForm(data=request.POST)
        if formulario_contacto.is_valid():
            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")
        
            email = EmailMessage(
                subject=f"Mensaje de {name}: {subject} - CNC Royal Icyng",
                body=f"{message}",
                to=[EMAIL_HOST_USER],
                reply_to=[email])
            
            print(email)

            
            try:
                email.send()
                return redirect("/contacto/?mensajeEnviado")
            except:
                return redirect("/contacto/?error")
            
    context={'form':contact_form,
            'team': team,
            'galleries': gallery_data}

    return render(request, 'index.html', context=context)
