from django import forms
from .models import Premio, Publicidad

class PublicidadForm(forms.ModelForm):
    class Meta:
        model = Publicidad
        fields = ['imagen', 'descripcion']

class PremioForm(forms.ModelForm):
    class Meta:
        model = Premio
        fields = ['nombre', 'descripcion', 'imagen', 'categoria']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }
