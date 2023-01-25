from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Pqrsdf, PqrsdfState
from .forms import PqrsdfForm
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
        if self.request.GET.get("search") != None:
            queryset = self.request.GET.get("search")
            queryset = Pqrsdf.objects.filter(
                active=True, radicated__icontains=queryset) | Pqrsdf.objects.filter(active=True, type_pqrsdf__icontains=queryset)
        return queryset


class DetailPqrsdf(DetailView):
    model = Pqrsdf
    template_name = 'pqrsdf/detail_pqrsdf.html'
    context_object_name = 'pqrsdfs'


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
# def Home(request):
#     return render(request, 'index.html')


# def Login(request):
#     return render(request, 'login.html')

# def Dashboard(request):
#     return render(request, 'dashboard.html')

# def createPqrsdf(request):
#     if request.method == 'POST':
#         pqrsdf_form = PqrsdfForm(request.POST)
#         if pqrsdf_form.is_valid():
#             pqrsdf_form.save()
#             return redirect('pqrsdf:get_pqrsdfs')
#     else:
#         pqrsdf_form = PqrsdfForm()
#     return render(request, 'pqrsdf/create_pqrsdf.html', {'pqrsdf_form': pqrsdf_form})


# def getPqrsdfs(request):
#     queryset = request.GET.get("search")
#     pqrsdfs = Pqrsdf.objects.filter(active=True)
#     if queryset:
#         pqrsdfs = Pqrsdf.objects.filter(
#             Q(type_pqrsdf__icontains=queryset),
#             active=True
#         ).distinct()
#     # Recibe el objeto, y cuanto quiere mostrar por página
#     paginator = Paginator(pqrsdfs, 10)
#     page = request.GET.get('page')  # Obtiene la página actual
#     # Recibe el valor de la página y carga las pqrsdf correspondientes a esa página
#     pqrsdfs = paginator.get_page(page)
#     return render(request, 'pqrsdf/get_pqrsdfs.html',  {'pqrsdfs': pqrsdfs})

# def updatePqrsdf(request, id):
#     pqrsdf_form = None
#     error = None
#     try:
#         pqrsdf = Pqrsdf.objects.get(id=id)
#         if request.method == 'GET':
#             pqrsdf_form = PqrsdfForm(instance=pqrsdf)
#         else:
#             pqrsdf_form = PqrsdfForm(request.POST, instance=pqrsdf)
#             if pqrsdf_form.is_valid():
#                 pqrsdf_form.save()
#                 return redirect('pqrsdf:get_pqrsdfs')
#     except ObjectDoesNotExist as e:
#         error = e

#     return render(request, 'pqrsdf/create_pqrsdf.html', {'pqrsdf_form': pqrsdf_form, 'error': error})


# def deletePqrsdf(request, id):
#     pqrsdf = Pqrsdf.objects.get(id=id)
#     if request.method == "POST":
#         pqrsdf.active = False
#         pqrsdf.save()
#         return redirect('pqrsdf:get_pqrsdfs')
#     return render(request, 'pqrsdf/delete_pqrsdf.html', {'pqrsdf': pqrsdf})
