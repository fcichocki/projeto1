from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1, choices=[
                            ('M', 'Masculino'), ('F', 'Feminino')])
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    endereco = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    usuario = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nome
