from django.shortcuts import render, redirect, get_object_or_404
from .models import Convenio
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_convenio(request):
    convenios = Convenio.objects.filter(usuario=request.user.username)

    if request.method == 'POST':
        nome_convenio = request.POST.get('nome')
        Convenio.objects.create(
            nome=nome_convenio, usuario=request.user.username)
        return redirect('cadastrar_convenio')

    return render(request, 'cadastrar_convenio.html', {'convenios': convenios})


def excluir_convenio(request, id_convenio):
    convenio = get_object_or_404(Convenio, id=id_convenio)
    convenio.delete()
    return redirect('cadastrar_convenio')
