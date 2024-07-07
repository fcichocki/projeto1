from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import DadosConsultorio


@login_required
def cadastrar_dados_consultorio(request):
    user = request.user

    try:
        dados = DadosConsultorio.objects.get(usuario=user.username)
    except DadosConsultorio.DoesNotExist:
        dados = None

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')
        cep = request.POST.get('cep')

        if dados:
            # Atualizar dados existentes
            dados.nome = nome
            dados.cpf_cnpj = cpf_cnpj
            dados.telefone = telefone
            dados.email = email
            dados.endereco = endereco
            dados.cep = cep
            dados.save()
        else:
            # Criar novos dados
            DadosConsultorio.objects.create(
                nome=nome,
                cpf_cnpj=cpf_cnpj,
                telefone=telefone,
                email=email,
                endereco=endereco,
                cep=cep,
                usuario=user.username  # Preencher campo usuario
            )
        # Redirecionar para a mesma página após salvar
        return redirect(reverse_lazy('cadastro_consultorio'))

    return render(request, 'cadastrar_consultorio.html', {'dados': dados})
