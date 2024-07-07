from django.db import models


class Convenio(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nome
