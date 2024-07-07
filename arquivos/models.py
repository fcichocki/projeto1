from django.db import models
# Substitua 'pacientes' pelo nome correto do seu app de pacientes
from pacientes.models import Paciente


class Arquivo(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name='arquivos')
    arquivo = models.FileField(upload_to='pacientes_arquivos/')

    def __str__(self):
        return f"{self.paciente.nome} - {self.arquivo.name}"
