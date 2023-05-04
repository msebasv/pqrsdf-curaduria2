from django.db import models
from apps.user.models import User
from datetime import datetime, timezone, date
from workalendar.america import Colombia

cal = Colombia()
# Create your models here.

class Pqrsdf(models.Model):
    STATE_OPTIONS = (
        (1, "Radicación"),
        (2, "Elaboración"),
        (3, "Revisión"),
        (4, "Finalizado"),
    )
    TYPE_PQRSDF = (
        (1, "Petición"),
        (2, "Queja/Reclamo"),
        (3, "Solicitud de información"),
        (4, "Denuncia"),
        (5, "Sugerencia/Propuesta")
    )
    TYPE_IDENTIFICATION = (
        (1, "Cédula de ciudadanía"),
        (2, "NUIP"),
        (3, "Cédula de extranjería"),
        (4, "NIT"),
        (5, "Pasaporte")
    )
    MEDIUM_CONTACT = (
        (1, "Correo electrónico"),
        (2, "Dirección de correspondencia"),
    )
    active = models.BooleanField(verbose_name="Activo", default=True)
    radicated = models.CharField(
        verbose_name="Radicado", max_length=50, blank=True, null=True)
    date_pqrsdf = models.DateTimeField(verbose_name="Fecha", auto_now_add=True)
    state_actual = models.IntegerField(verbose_name="Estado",
                             choices=STATE_OPTIONS, default=1)
    days_passed = models.IntegerField(verbose_name="Tiempo transcurrido", blank=True, null=True)
    type_pqrsdf = models.IntegerField(
        choices=TYPE_PQRSDF, verbose_name="Tipo de PQRSDF")
    type_anonymous = models.BooleanField(blank=True, null=True)
    name = models.CharField(
        max_length=30, verbose_name="Nombre", blank=True, null=True)
    type_identification = models.IntegerField(
        choices=TYPE_IDENTIFICATION, verbose_name="Tipo de identificación", blank=True, null=True)
    identification = models.CharField(
        max_length=30, verbose_name="Identificación", blank=True, null=True)
    medium_contact = models.IntegerField(
        choices=MEDIUM_CONTACT, verbose_name="Medio de contacto", blank=True, null=True)
    email = models.CharField(
        max_length=200, verbose_name="Correo electrónico", blank=True, null=True)
    correspondence_address = models.CharField(
        max_length=200, verbose_name="Dirección de correspondencia", blank=True, null=True)
    neighborhood = models.CharField(
        max_length=200, verbose_name="Barrio / Vereda / Corregimiento", blank=True, null=True)
    municipality = models.CharField(
        max_length=200, verbose_name="Municipio / Distrito", blank=True, null=True)
    country = models.CharField(
        max_length=200, verbose_name="País", blank=True, null=True)
    number_contact = models.CharField(
        max_length=30, verbose_name="Número de contacto", blank=True, null=True)
    description = models.TextField(verbose_name="Descripción")
    file_id = models.ForeignKey('PqrsdfFile', verbose_name="Adjunto", related_name='pqrsdf_files', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = "Pqrsdf"
        verbose_name_plural = "Pqrsdf"
        
    @staticmethod
    def filter_by_type(type_pqrsdf):
        return Pqrsdf.objects.filter(type_pqrsdf=type_pqrsdf)
    
    @staticmethod
    def filter_by_state(state_actual):
        return Pqrsdf.objects.filter(state_actual=state_actual)
    
    @property
    def days_since_created(self):
        """
        Calcula los días transcurridos desde la creación del objeto `Pqrsdf` hasta la fecha actual.
        """
        if not self.date_pqrsdf:
            return 0
        days_passed = cal.get_working_days_delta(self.date_pqrsdf.date(), date.today())
        return days_passed #Compara con 0 y así nunca regresa un número negativo

    def __str__(self):
        return str(self.type_pqrsdf)

class PqrsdfFile(models.Model):
    pqrsdf = models.ForeignKey(Pqrsdf, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pqrsdf_files/')
    
    class Meta:
        verbose_name = "PqrsdfFile"
        verbose_name_plural = "PqrsdfFile"
    
    def __str__(self):
        return f"{self.id}"
        
    @property
    def file_url(self):
        return self.file.url


class PqrsdfState(models.Model):
    id_pqrsdf = models.ForeignKey(
        Pqrsdf, on_delete=models.CASCADE, verbose_name="Id pqrsdf")
    state = models.IntegerField(choices=Pqrsdf.STATE_OPTIONS, default=1)
    date_previous_change = models.DateTimeField(verbose_name="Fecha anterior",null=True)
    date_change = models.DateTimeField(
        verbose_name="Fecha Actual", null=True, blank=True, auto_now=True)
    user_previous_change = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario Anterior', null=True, related_name='%(class)s_previous_change')
    user_change = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Usuario Actual", related_name='%(class)s_change', null=True)

    class Meta:
        verbose_name = 'PqrsdfState'
        verbose_name_plural = "PqrsdfStates"
    
        
    def __str__(self):
        return self.get_state_display()


class ResponsePqrsdf(models.Model):
    pqrsdf = models.ForeignKey(Pqrsdf, on_delete=models.CASCADE, verbose_name='Respuesta')
    date_creation = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True)
    user_response = models.ForeignKey(User, on_delete=models.PROTECT,verbose_name="Usuario")
    
    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"