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
        # widgets = {
        #     'type_pqrsdf': forms.CharField(
        #         widget=forms.Select(choices=CHOICES)
        #     ),
        # }
