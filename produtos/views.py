from decimal import Decimal
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_e_listar_produtos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade') or 0
        valor = request.POST.get('valor')
        usuario = request.user.username  # Obtém o nome do usuário logado

        if nome and valor:  # Certifique-se de que os campos obrigatórios estão preenchidos
            Produto.objects.create(
                # Preenche o campo "usuario"
                nome=nome, quantidade=quantidade, valor=valor, usuario=usuario
            )

        return redirect('cadastrar_e_listar_produtos')

    produtos = Produto.objects.filter(usuario=request.user.username)
    return render(request, 'cadastrar_e_listar_produtos.html', {'produtos': produtos})


@require_POST
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    return redirect('cadastrar_e_listar_produtos')


def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade')
        valor_str = request.POST.get('valor').replace(',', '.')

        valor = None
        try:
            valor = Decimal(valor_str)
        except InvalidOperation:
            pass  # Aqui você pode tratar o erro, como retornar uma mensagem para o formulário

        if nome and valor is not None:
            produto.nome = nome
            produto.quantidade = quantidade if quantidade else produto.quantidade
            produto.valor = valor
            produto.save()

            return redirect('cadastrar_e_listar_produtos')

    return render(request, 'editar_produto.html', {'produto': produto})
