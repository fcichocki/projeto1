from django.db import models
from pacientes.models import Paciente
from django.utils import timezone


class Atestado(models.Model):
    # Código Internacional de Doenças
    cid = models.CharField(max_length=10, verbose_name='CID')
    descricao = models.TextField(verbose_name='Descrição')

    def __str__(self):
        return f'{self.cid} - {self.descricao}'


class AtestadoPaciente(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, verbose_name='Paciente')
    atestado = models.TextField(verbose_name='Atestado')
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Atestado de {self.paciente.nome} em {self.data_hora}'
