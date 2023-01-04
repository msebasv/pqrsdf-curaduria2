from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import PqrsdfForm
from .models import Pqrsdf
# Create your views here.


def Home(request):
    return render(request, 'index.html')


def createPqrsdf(request):
    if request.method == 'POST':
        pqrsdf_form = PqrsdfForm(request.POST)
        if pqrsdf_form.is_valid():
            pqrsdf_form.save()
            return redirect('pqrsdf:get_pqrsdfs')
    else:
        pqrsdf_form = PqrsdfForm()
    return render(request, 'pqrsdf/create_pqrsdf.html', {'pqrsdf_form': pqrsdf_form})


def getPqrsdfs(request):
    pqrsdfs = Pqrsdf.objects.filter(active=True)
    return render(request, 'pqrsdf/get_pqrsdfs.html',  {'pqrsdfs': pqrsdfs})


def updatePqrsdf(request, id):
    pqrsdf_form = None
    error = None
    try:
        pqrsdf = Pqrsdf.objects.get(id=id)
        if request.method == 'GET':
            pqrsdf_form = PqrsdfForm(instance=pqrsdf)
        else:
            pqrsdf_form = PqrsdfForm(request.POST, instance=pqrsdf)
            if pqrsdf_form.is_valid():
                pqrsdf_form.save()
                return redirect('pqrsdf:get_pqrsdfs')
    except ObjectDoesNotExist as e:
        error = e

    return render(request, 'pqrsdf/create_pqrsdf.html', {'pqrsdf_form': pqrsdf_form, 'error': error})


def deletePqrsdf(request, id):
    pqrsdf = Pqrsdf.objects.get(id=id)
    if request.method == "POST":
        pqrsdf.active = False
        pqrsdf.save()
        return redirect('pqrsdf:get_pqrsdfs')
    return render(request, 'pqrsdf/delete_pqrsdf.html', {'pqrsdf': pqrsdf})
