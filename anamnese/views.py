from django.shortcuts import render, redirect, get_object_or_404
from .models import Anamnese


from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .models import Anamnese
from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_anamnese(request):
    if request.method == 'POST':
        texto_anamnese = request.POST.get('anamnese')
        Anamnese.objects.create(anamnese=texto_anamnese, usuario=request.user)
        return redirect('cadastrar_anamnese')

    anamneses = Anamnese.objects.filter(usuario=request.user)
    return render(request, 'cadastrar_anamnese.html', {'anamneses': anamneses})


def excluir_anamnese(request, id):
    anamnese = get_object_or_404(Anamnese, id=id)
    if request.method == 'POST':
        anamnese.delete()
        return redirect('cadastrar_anamnese')
    return render(request, 'cadastrar_anamnese.html')


def editar_anamnese(request, id):
    anamnese_item = get_object_or_404(Anamnese, id=id)

    if request.method == 'POST':
        anamnese_texto = request.POST.get('anamnese')
        anamnese_item.anamnese = anamnese_texto
        anamnese_item.save()
        return redirect('cadastrar_anamnese')

    return render(request, 'editar_anamnese.html', {'anamnese': anamnese_item})
