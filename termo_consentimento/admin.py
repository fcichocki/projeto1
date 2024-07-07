from django.contrib import admin
from .models import TermoConsentimento
from .models import ConsentimentoPaciente

admin.site.register(TermoConsentimento)
admin.site.register(ConsentimentoPaciente)
