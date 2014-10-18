from django.contrib import admin
from sap.models import Procedimento

class ProcedimentoAdmin(admin.ModelAdmin):
	list_display = ['interessado', 'email', 'telefone']
	list_display_links = ['interessado', 'email', 'telefone']
	list_filter = ['criado_em', 'modificado_em']
	ordering = ['interessado', 'email', 'telefone']
	search_fields = ['interessado', 'email', 'telefone']

admin.site.register(Procedimento, ProcedimentoAdmin)
