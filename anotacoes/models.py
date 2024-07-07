from django.db import models

from pacientes.models import Paciente


class Anotacao(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    anotacoes = models.TextField(max_length=3000, verbose_name="Anotações")

    def __str__(self):
        return f"Anotações de {self.paciente.nome}"
