# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Assunto, Inspetoria, Situacao, Procedimento, Exigencia
from .forms import ProcedimentoForm, ExigenciaForm

class AssuntoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    ordering = ['nome']
    search_fields = ['nome']


class InspetoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    ordering = ['nome']
    search_fields = ['nome']


class SituacaoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    ordering = ['nome']
    search_fields = ['nome']


class ExigenciaInline(admin.StackedInline):
    model = Exigencia
    form = ExigenciaForm
    extra = 1
    fieldsets = [
        ('Exigência', {
            'classes': ['collapse'],
            'fields': (
                'conteudo',
                'atendida',
            )
        })
    ]


class ProcedimentoAdmin(admin.ModelAdmin):
    form = ProcedimentoForm
    list_display = ['id', 'interessado', 'auditor_responsavel', 'situacao', 'data_de_abertura']
    list_display_links = ['interessado', 'auditor_responsavel', 'situacao', 'data_de_abertura']
    list_filter = ['data_de_abertura', 'modificado_em', 'situacao']
    ordering = ['interessado', 'auditor_responsavel', 'situacao', 'data_de_abertura']
    search_fields = ['interessado']
    inlines = [ExigenciaInline]


admin.site.register(Procedimento, ProcedimentoAdmin)
admin.site.register(Inspetoria, InspetoriaAdmin)
admin.site.register(Assunto, AssuntoAdmin)
admin.site.register(Situacao, SituacaoAdmin)

