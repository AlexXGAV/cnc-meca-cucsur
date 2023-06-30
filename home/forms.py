from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='name', required=True, max_length=40,
                            widget=forms.TextInput(attrs={'placeholder': 'Tu nombre',
                                                             'class':'form-control',
                                                             'id':'name'}))
    email = forms.EmailField(label='email', required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Tu email',
                                                             'class':'form-control',
                                                             'id':'email'}))
    subject = forms.CharField(label='subject', required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Tema',
                                                             'class':'form-control',
                                                             'id':'subject'}))
    message = forms.CharField(label='message', required=True,
                                widget=forms.Textarea(attrs={'placeholder': 'Mensaje',
                                                             'class':'form-control',
                                                             'rows':'5'}))
