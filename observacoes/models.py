from django.db import models
# Ajuste o caminho do import conforme a localização do seu modelo Paciente
from pacientes.models import Paciente


class Observacao(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, verbose_name='Paciente')
    observacoes = models.TextField(
        max_length=1000, blank=True, verbose_name='Observações')

    def __str__(self):
        return f'Observações para {self.paciente.nome}'
