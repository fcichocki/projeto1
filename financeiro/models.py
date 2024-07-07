from django.db import models
from pacientes.models import Paciente
from produtos.models import Produto


class Receita(models.Model):
    cliente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, verbose_name='Cliente')
    descricao = models.ForeignKey(Produto, on_delete=models.CASCADE,
                                  verbose_name='Descrição', related_name='descricao_receita')
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor')
    data = models.DateField(verbose_name='Data')
    status = models.CharField(max_length=100, verbose_name='Status')
    forma_pagamento = models.CharField(
        max_length=100, verbose_name='Forma de Pagamento')

    usuario = models.CharField(
        max_length=15, blank=True, verbose_name='Usuário')

    def __str__(self):
        return f'Receita {self.descricao} para {self.cliente}'


class Despesa(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    data = models.DateField(verbose_name="Data")
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor")

    usuario = models.CharField(
        max_length=15, blank=True, verbose_name='Usuário')

    def __str__(self):
        return f"{self.descricao} - {self.data} - {self.valor}"
