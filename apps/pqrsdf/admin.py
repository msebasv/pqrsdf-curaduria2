from django.contrib import admin
from .models import Pqrsdf, PqrsdfState
# Register your models here.


class PqrsdfAdmin(admin.ModelAdmin):
    search_fields = ['type_pqrsdf', 'radicated']
    list_display = ('radicated', 'type_pqrsdf',
                    'date_pqrsdf', 'type_anonymous', 'state')


class PqrsdfStateAdmin(admin.ModelAdmin):
    list_display = ('id_pqrsdf', 'date_input',
                    'date_output', 'user_change_input', 'user_change_output')


admin.site.register(Pqrsdf, PqrsdfAdmin)
admin.site.register(PqrsdfState, PqrsdfStateAdmin)
