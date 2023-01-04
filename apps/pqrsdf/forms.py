from django import forms
from .models import Pqrsdf


class PqrsdfForm(forms.ModelForm):
    class Meta:
        model = Pqrsdf
        fields = ['type_pqrsdf', 'type_anonymous',
                  'name', 'type_identification', 'identification', 'medium_contact', 'number_contact', 'number_contact', 'description']
