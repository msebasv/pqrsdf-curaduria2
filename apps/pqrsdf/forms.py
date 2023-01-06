from django import forms
from .models import Pqrsdf


class PqrsdfForm(forms.ModelForm):
    class Meta:
        model = Pqrsdf
        fields = ['type_pqrsdf', 'type_anonymous', 'name', 'type_identification',
                  'identification', 'medium_contact', 'number_contact', 'description']
        labels = {
            'type_pqrsdf': 'Tipo de PQRSDF',
            'type_anonymous': 'Anónimo',
            'name': 'Nombre',
            'type_identification': 'Tipo de identificación',
            'identification': 'Identificación',
            'medium_contact': 'Medio de contacto',
            'number_contact': 'Número de contacto',
            'description': 'Descripción'
        }
        widgets = {
            'type_pqrsdf': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'type_anonymous': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'type_identification': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'identification': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'medium_contact': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'number_contact': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
        # widgets = {
        #     'type_pqrsdf': forms.CharField(
        #         widget=forms.Select(choices=CHOICES)
        #     ),
        # }
