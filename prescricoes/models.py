
from django.db import models
from pacientes.models import Paciente


class Prescricao(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name='prescricoes')
    prescricoes = models.CharField(max_length=500)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prescrição para {self.paciente.nome} em {self.data_hora}'
