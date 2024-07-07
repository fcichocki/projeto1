from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TermoConsentimento
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_termo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        termo_consentimento = request.POST.get('termo_consentimento')
        usuario = request.user.username  # Obtém o nome de usuário do usuário logado

        TermoConsentimento.objects.create(
            nome=nome, termo_consentimento=termo_consentimento, usuario=usuario)
        messages.success(
            request, 'Termo de consentimento cadastrado com sucesso.')
        return redirect('listar_termos')

    return render(request, 'cadastrar_termo.html')


def editar_termo(request, id):
    termo = get_object_or_404(TermoConsentimento, id=id)

    if request.method == 'POST':
        termo.nome = request.POST.get('nome')
        termo.termo_consentimento = request.POST.get('termo_consentimento')
        termo.save()

        messages.success(
            request, 'Termo de consentimento atualizado com sucesso.')
        return redirect('listar_termos')

    return render(request, 'editar_termo.html', {'termo': termo})


def excluir_termo(request, id):
    termo = get_object_or_404(TermoConsentimento, id=id)

    if request.method == 'POST':
        termo.delete()
        messages.success(
            request, 'Termo de consentimento excluído com sucesso.')
        return redirect('listar_termos')

    return render(request, 'excluir_termo.html', {'termo': termo})


def listar_termos(request):
    termos = TermoConsentimento.objects.filter(usuario=request.user.username)
    return render(request, 'listar_termos.html', {'termos': termos})
