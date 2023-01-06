from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .forms import PqrsdfForm
from .models import Pqrsdf
# Create your views here.


class Home(TemplateView):
    template_name = 'index.html'


class Dashboard(TemplateView):
    template_name = 'dashboard.html'


class GetPqrsdfs(ListView):
    model = Pqrsdf
    template_name = 'pqrsdf/get_pqrsdfs.html'
    context_object_name = 'pqrsdfs'
    queryset = Pqrsdf.objects.filter(active=True)


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
