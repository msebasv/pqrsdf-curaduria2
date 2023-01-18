from django.db import models

# Create your models here.


class Pqrsdf(models.Model):
    STATE = (
        ("Radicacion", "Radicación"),
        ("Elaboracion", "Elaboración"),
        ("Revision", "Revisión"),
        ("Finalizado", "Finalizado"),
    )
    TYPE_PQRSDF = (
        ("Peticion", "Petición"),
        ("Queja", "Queja/Reclamo"),
        ("Solicitud", "Solicitud de información"),
        ("Denuncia", "Denuncia"),
        ("Sugerencia", "Sugerencia/Propuesta")
    )
    TYPE_IDENTIFICATION = (
        ("CC", "Cédula de ciudadanía"),
        ("NU", "NUIP"),
        ("CE", "Cédula de extranjería"),
        ("NIT", "NIT"),
        ("PS", "Pasaporte")
    )
    MEDIUM_CONTACT = (
        ("CE", "Correo electrónico"),
        ("DC", "Dirección de correspondencia"),
    )
    active = models.BooleanField(verbose_name="Activo", default=True)
    date_pqrsdf = models.DateTimeField(verbose_name="Fecha", auto_now_add=True)
    state = models.CharField(verbose_name="Estado",
                             max_length=100, choices=STATE, default='Radicacion')
    type_pqrsdf = models.CharField(
        max_length=10, choices=TYPE_PQRSDF, verbose_name="Tipo de PQRSDF")
    type_anonymous = models.BooleanField(blank=True, null=True)
    name = models.CharField(
        max_length=30, verbose_name="Nombre", blank=True, null=True)
    type_identification = models.CharField(
        max_length=3, choices=TYPE_IDENTIFICATION, verbose_name="Tipo de identificación", blank=True, null=True)
    identification = models.CharField(
        max_length=30, verbose_name="Identificación", blank=True, null=True)
    medium_contact = models.CharField(
        max_length=2, choices=MEDIUM_CONTACT, verbose_name="Medio de contacto", blank=True, null=True)
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

    class Meta:
        verbose_name = "Pqrsdf"
        verbose_name_plural = "Pqrsdf"

    def __str__(self):
        return self.type_pqrsdf


class PqrsdfState(models.Model):
    id_pqrsdf = models.ForeignKey(
        Pqrsdf, null=True, blank=True, on_delete=models.CASCADE)
    date_input = models.DateField(
        verbose_name="Fecha Entrada", null=True, blank=True)
    date_output = models.DateField(
        verbose_name="Fecha Salida", null=True, blank=True)
    user_change_input = models.CharField(
        max_length=191, verbose_name="Usuario entrada", null=True,  blank=True)
    user_change_output = models.CharField(
        max_length=10, verbose_name="Usuario Salida", null=True,  blank=True)

    class Meta:
        verbose_name = 'PqrsdfState'
        verbose_name_plural = "PqrsdfStates"
