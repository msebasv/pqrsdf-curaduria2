from django.contrib import admin
from .models import Pqrsdf, PqrsdfState
# Register your models here.


class PqrsdfAdmin(admin.ModelAdmin):
    search_fields = ['type_pqrsdf']
    list_display = ('type_pqrsdf', 'date_pqrsdf', 'type_anonymous')


admin.site.register(Pqrsdf, PqrsdfAdmin)
admin.site.register(PqrsdfState)
