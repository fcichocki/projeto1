from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nome
