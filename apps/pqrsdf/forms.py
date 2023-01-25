from django import forms
from .models import Pqrsdf, PqrsdfState


class PqrsdfForm(forms.ModelForm):
    class Meta:
        model = Pqrsdf
        fields = ['type_pqrsdf', 'type_anonymous', 'name', 'type_identification',
                  'identification', 'medium_contact', 'email', 'correspondence_address', 'neighborhood', 'municipality', 'country', 'number_contact', 'description']
        labels = {
            'type_pqrsdf': 'Tipo de PQRSDF',
            'type_anonymous': 'Anónimo',
            'name': 'Nombre',
            'type_identification': 'Tipo de identificación',
            'identification': 'Identificación',
            'medium_contact': 'Medio de contacto',
            'email': 'Correo electrónico',
            'correspondence_address': 'Dirección de correspondencia',
            'neighborhood': 'Barrio / Vereda / Corregimiento',
            'municipality': 'Municipio / Distrito',
            'country': 'País',
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
                    'id': 'id_anon',
                    'class': 'form-check-input',
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
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'correspondence_address': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'neighborhood': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'municipality': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'country': forms.TextInput(
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
