from django.shortcuts import render, redirect, get_object_or_404
from .models import Profissional
from convenios.models import Convenio


from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_profissional(request):
    convenios = Convenio.objects.filter(usuario=request.user)
    # Filtra os profissionais pelo usuário logado
    profissionais = Profissional.objects.filter(usuario=request.user.username)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        cep = request.POST.get('cep')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        convenios_selecionados = request.POST.getlist('convenios')
        usuario = request.user.username  # Obtém o nome de usuário do usuário logado

        profissional = Profissional.objects.create(
            nome=nome, endereco=endereco, cep=cep, cpf_cnpj=cpf_cnpj,
            telefone=telefone, email=email, usuario=usuario
        )
        profissional.convenios.set(convenios_selecionados)
        profissional.save()

        return redirect('cadastrar_profissional')

    return render(request, 'cadastrar_profissional.html', {
        'convenios': convenios,
        'profissionais': profissionais
    })


def excluir_profissional(request, id_profissional):
    profissional = get_object_or_404(Profissional, id=id_profissional)
    if request.method == 'POST':
        profissional.delete()
        return redirect('cadastrar_profissional')
    return render(request, 'confirmar_exclusao.html', {'profissional': profissional})


def editar_profissional(request, id_profissional):
    profissional = get_object_or_404(Profissional, id=id_profissional)
    convenios = Convenio.objects.all()

    if request.method == 'POST':
        profissional.nome = request.POST.get('nome')
        profissional.endereco = request.POST.get('endereco')
        profissional.cep = request.POST.get('cep')
        profissional.cpf_cnpj = request.POST.get('cpf_cnpj')
        profissional.telefone = request.POST.get('telefone')
        profissional.email = request.POST.get('email')
        profissional.save()

        convenios_selecionados = request.POST.getlist('convenios')
        profissional.convenios.set(convenios_selecionados)

        return redirect('cadastrar_profissional')

    return render(request, 'editar_profissional.html', {
        'profissional': profissional,
        'convenios': convenios
    })
