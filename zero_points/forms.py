from django import forms
from .models import GcodeFile, Machine

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = GcodeFile
        fields = ["name", "file", "machine", "radius_cookie"]
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Mi Trabajo 1',
                                                             'class':'form-control',
                                                             'id':'name'}),
            "radius_cookie": forms.NumberInput(attrs={'placeholder': '5 mm',
                                                             'class':'form-control',
                                                             'id':'radius_cookie'}),
            "file": forms.FileInput(attrs={'placeholder': 'example1.gcode',
                                                             'class':'form-control',
                                                             'id':'file'
                                                             }),
            "converted_file": forms.HiddenInput(attrs={'placeholder': 'example2.gcode',
                                                             'class':'form-control',
                                                             'id':'converted_file'
                                                             }),
            "machine": forms.Select(attrs={'option value selected': '1',
                                                             'class':'form-control',
                                                             'id':'machine'})
        
        }
