from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Pqrsdf, PqrsdfState
from .forms import PqrsdfForm, StateForm
from django.db.models import F, Q
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
# Create your views here.


class Home(TemplateView):
    template_name = 'index.html'


class Dashboard(TemplateView):
    template_name = 'dashboard.html'


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
        return queryset


class DetailPqrsdf(DetailView):
    model = Pqrsdf
    template_name = 'pqrsdf/detail_pqrsdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pqrsdf = self.object
        pqrsdf_states = PqrsdfState.objects.filter(id_pqrsdf=pqrsdf).order_by(F('date_change').desc(nulls_last=True))
        context['pqrsdf_states'] = pqrsdf_states
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
        self.object.start_date = make_aware(datetime.now())
        self.object.save()
        
        # Asignar número de días a la instancia del modelo Pqrsdf
        start_date = self.object.start_date
        current_date = make_aware(datetime.now())
        days_passed = current_date - start_date
        self.object.days_passed = days_passed if days_passed else timedelta(0)
        self.object.save()
        
        context = self.get_context_data()
        context['days_passed'] = self.object.days_passed
        # Crear objeto PqrsdfState
        pqrsdfstate = PqrsdfState(
            id_pqrsdf=self.object,
            state=Pqrsdf.STATE_OPTIONS[0][0], # Estado de Radicación
            user_change=self.request.user
        )
        pqrsdfstate.save()
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
