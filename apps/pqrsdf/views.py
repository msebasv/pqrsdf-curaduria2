from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from .models import Pqrsdf, PqrsdfState, PqrsdfFile
from .forms import PqrsdfForm, StateForm
from django.db.models import F, Q
from django.http import HttpResponse, Http404, FileResponse
from django.contrib.auth import get_user_model
import os
from django.conf import settings

# Create your views here.


class Home(TemplateView):
    template_name = 'index.html'


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Pqrsdf.objects.all()
        estado_counts = {
            'Radicación': queryset.filter(state_actual=1).count(),
            'Elaboración': queryset.filter(state_actual=2).count(),
            'Revisión': queryset.filter(state_actual=3).count(),
            'Finalizado': queryset.filter(state_actual=4).count(),
            # You can add more states here if necessary
        }
        type_counts = {
            'Petición':queryset.filter(type_pqrsdf=1).count(),
            'Queja/Reclamo':queryset.filter(type_pqrsdf=2).count(),
            'Solicitud de información':queryset.filter(type_pqrsdf=3).count(),
            'Denuncia':queryset.filter(type_pqrsdf=4).count(),
            'Sugerencia/Propuesta':queryset.filter(type_pqrsdf=5).count(),
        }
        context['estado_counts'] = estado_counts
        context['type_counts'] = type_counts
        return context




class GetPqrsdfs(ListView):
    """Gets the list of pqrsdf
        Method: get_queryset
        Function: 
        * Obtain all pqrsdf if "Active" is true and order by date_pqrsdf
        * In the second filter, in the conditional, it obtains the pqrsdfs that are placed in the search field and searches it by root or by type.
    """
    model = Pqrsdf
    template_name = 'pqrsdf/get_pqrsdfs.html'
    context_object_name = 'pqrsdfs'
    paginate_by = 20

    def get_queryset(self):
        queryset = Pqrsdf.objects.filter(active=True).order_by('-date_pqrsdf')
        search_query = self.request.GET.get("search")
        if search_query:
            radicated_filter = Q(radicated__icontains=search_query)
            type_filter = Q(type_pqrsdf__icontains=search_query)
            state_filter = Q(state_actual__icontains=search_query)
            queryset = queryset.filter(radicated_filter | type_filter | state_filter)
        type_pqrsdf = self.request.GET.get("type_pqrsdf")
        state_actual = self.request.GET.get("state_actual")
        if type_pqrsdf:
            if type_pqrsdf == 'Todos':
                pass
            else:
                queryset = Pqrsdf.filter_by_type(type_pqrsdf)
        if state_actual:
            if state_actual == 'Todos':
                pass
            else:
                queryset = Pqrsdf.filter_by_state(state_actual)
            # Actualizar el valor de days_passed
        for pqrsdf in queryset:
            pqrsdf.days_passed = pqrsdf.days_since_created
            pqrsdf.save()
        return queryset
    
class DownloadFileView(View):
    def get(self, request, pk):
        pqrsdf = get_object_or_404(Pqrsdf, pk=pk)
        pqrsdf_file = pqrsdf.file_id
        if pqrsdf_file:
            file_path = pqrsdf_file.file.path
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404('El archivo no existe')


class DetailPqrsdf(DetailView):
    model = Pqrsdf
    template_name = 'pqrsdf/detail_pqrsdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pqrsdf = self.object
        pqrsdf_states = PqrsdfState.objects.filter(id_pqrsdf=pqrsdf).order_by(F('date_change').desc(nulls_last=True))
        context['pqrsdf_states'] = pqrsdf_states
        pqrsdf_file = pqrsdf.file_id
        file_name = pqrsdf_file.file.name if pqrsdf_file else ''

        fields = {
            'Tipo': {'value': pqrsdf.get_type_pqrsdf_display(), 'class': 'type-pqrsdf'},
            'Estado': {'value': pqrsdf.get_state_actual_display(), 'class': 'state-pqrsdf'},
            'Nombre': {'value': pqrsdf.name, 'class': 'none'},
            'Tipo de identificación': {'value': pqrsdf.get_type_identification_display(), 'class': 'none'},
            'Identificación': {'value': pqrsdf.identification, 'class': 'none'},
            'Correo electrónico': {'value': pqrsdf.email, 'class': 'none'},
            'Dirección de correspondencia': {'value': pqrsdf.correspondence_address, 'class': 'none'},
            'Barrio / Vereda / Corregimiento': {'value': pqrsdf.neighborhood, 'class': 'none'},
            'Municipio / Distrito': {'value': pqrsdf.municipality, 'class': 'none'},
            'País': {'value': pqrsdf.country, 'class': 'none'},
            'Número de contacto': {'value': pqrsdf.number_contact, 'class': 'none'},
            'Descripción': {'value': pqrsdf.description, 'class': 'none'},
        }
        # Agregar sólo aquellos campos que no estén vacíos o None al contexto "k" Hace referencia a la key y "v" hace referencia al value
        context['fields'] = {k: v for k, v in fields.items() if v.get('value', '')}
        return context

    
class UpdateState(UpdateView):
    model = Pqrsdf
    form_class = StateForm
    template_name = 'pqrsdf/update_state.html'
    success_url = reverse_lazy('pqrsdf:get_pqrsdfs')

    def form_valid(self, form):
        pqrsdf = form.save(commit=False)
        state_actual = form.cleaned_data['state_actual']

        pqrsdf_state = PqrsdfState.objects.filter(id_pqrsdf=pqrsdf).order_by('date_change').last()

        date_previous_change = pqrsdf_state.date_change if pqrsdf_state else None
        user_previous_change = pqrsdf_state.user_change if pqrsdf_state else None

        # Crear registro con el estado actual y los datos de cambio
        PqrsdfState.objects.create(
            id_pqrsdf=pqrsdf,
            state=state_actual,
            date_previous_change=date_previous_change,
            user_previous_change=user_previous_change,
            date_change=timezone.now(),
            user_change=self.request.user
        )

        return super().form_valid(form)

class ListStatePqrsdf(ListView):
    model = PqrsdfState
    template_name = 'pqrsdf/detail_pqrsdf.html'
    context_object_name = 'pqrsdfState'
    paginate_by = 20


class CreatePqrsdf(CreateView):
    model = Pqrsdf
    template_name = 'pqrsdf/create_pqrsdf.html'
    form_class = PqrsdfForm
    success_url = reverse_lazy('pqrsdf:get_pqrsdfs')
    
    def form_valid(self, form):
        # Asignar usuario actual
        form.instance.user = self.request.user
        
        # Generar radicado
        lastRadicate = Pqrsdf.objects.last()
        string = str(lastRadicate.radicated)
        separate = list(string.split("CU"))
        number = separate[-1]
        newNumber = int(number) + 1
        rad = str(newNumber)
        radNew = 'CU' + rad.zfill(3)
        form.instance.radicated = radNew
        
        # Guardar objeto Pqrsdf
        response = super().form_valid(form)
        
        pqrsdf = self.object
        pqrsdf.date_pqrsdf = timezone.now()
        pqrsdf.days_passed = pqrsdf.days_since_created
        pqrsdf.save()

        # Crear objeto PqrsdfState
        pqrsdfstate = PqrsdfState(
            id_pqrsdf=self.object,
            state=Pqrsdf.STATE_OPTIONS[0][0], # Estado de Radicación
            user_change=self.request.user
        )
        pqrsdfstate.save()
        
        # Obtener el archivo enviado por el usuario
        file = self.request.FILES.get('file')

        if file:
            # Crear objeto PqrsdfFile y guardar el archivo
            pqrsdf_file = PqrsdfFile(pqrsdf=pqrsdf, file=file)
            pqrsdf_file.save()

            # Actualizar la Pqrsdf con la referencia al archivo creado
            pqrsdf.file_id = pqrsdf_file
            pqrsdf.save()
        return response

class UpdatePqrsdf(UpdateView):
    model = Pqrsdf
    template_name = 'pqrsdf/create_pqrsdf.html'
    form_class = PqrsdfForm
    success_url = reverse_lazy('pqrsdf:get_pqrsdfs')


class DeletePqrsdf(DeleteView):
    """Desactivate option active
        Method: post
        Function: 
        * Obtain de pqrsdf by id or primary key and change de field from true to false, save de change and redirect to the list of pqrsdf 
    """
    model = Pqrsdf

    def post(self, request, pk, *args, **kwargs):
        object = Pqrsdf.objects.get(id=pk)
        object.active = False
        object.save()
        return redirect('pqrsdf:get_pqrsdfs')


class CreatePqrsdfUser(CreateView):
    model = Pqrsdf
    template_name = 'create_pqrsdfUser.html'
    form_class = PqrsdfForm
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        # Asignar usuario actual
        form.instance.user = None
        
        # Generar radicado
        lastRadicate = Pqrsdf.objects.last()
        string = str(lastRadicate.radicated)
        separate = list(string.split("CU"))
        number = separate[-1]
        newNumber = int(number) + 1
        rad = str(newNumber)
        radNew = 'CU' + rad.zfill(3)
        form.instance.radicated = radNew
        
        # Guardar objeto Pqrsdf
        response = super().form_valid(form)
        
        pqrsdf = self.object
        pqrsdf.date_pqrsdf = timezone.now()
        pqrsdf.days_passed = pqrsdf.days_since_created
        pqrsdf.save()

        # Crear objeto PqrsdfState
        pqrsdfstate = PqrsdfState(
            id_pqrsdf=self.object,
            state=Pqrsdf.STATE_OPTIONS[0][0], # Estado de Radicación
            user_change=None
        )
        pqrsdfstate.save()
        
        # Obtener el archivo enviado por el usuario
        file = self.request.FILES.get('file')

        if file:
            # Crear objeto PqrsdfFile y guardar el archivo
            pqrsdf_file = PqrsdfFile(pqrsdf=pqrsdf, file=file)
            pqrsdf_file.save()

            # Actualizar la Pqrsdf con la referencia al archivo creado
            pqrsdf.file_id = pqrsdf_file
            pqrsdf.save()
        return response

class GetPqrsdfView(View):
    def get(self, request, radicated):
        if radicated:
            try:
                pqrsdf = Pqrsdf.objects.get(radicated=radicated)
                return render(request, 'get_pqrsdf.html', {'pqrsdf': pqrsdf})
            except Pqrsdf.DoesNotExist:
                error_message = 'PQRSDF no encontrada'
        else:
            error_message = 'Número de radicado inválido'

        return render(request, 'get_pqrsdf.html', {'error_message': error_message})