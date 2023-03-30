from django.contrib import admin
from .models import Pqrsdf, PqrsdfState, ResponsePqrsdf
# Register your models here.


class PqrsdfAdmin(admin.ModelAdmin):
    search_fields = ['type_pqrsdf', 'radicated']
    list_display = ('radicated', 'type_pqrsdf',
                    'date_pqrsdf', 'type_anonymous', 'state_actual')

class PqrsdfStateAdmin(admin.ModelAdmin):
    list_display = ('id_pqrsdf', 'state', 'date_previous_change',
                    'date_change', 'user_previous_change','user_change')
    
class ResponsePqrsdfAdmin(admin.ModelAdmin):
    list_display = ('pqrsdf', 'date_creation',
                    'response', 'user_response')


admin.site.register(Pqrsdf, PqrsdfAdmin)
admin.site.register(PqrsdfState, PqrsdfStateAdmin)
admin.site.register(ResponsePqrsdf, ResponsePqrsdfAdmin)





