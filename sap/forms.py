# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm, ModelChoiceField, Select, TextInput
from suit.widgets import AutosizedTextarea
from .models import Exigencia, GrupoTrabalhoAuditor, Procedimento, Usuario_Inspetoria

class UserModelGrupoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            u = Usuario_Inspetoria.objects.get(user=obj)
            insp = u.inspetoria
        except:
            insp = " "
            pass

        return "[%s] %s" % (insp, obj.get_full_name())

# Possíveis opções para o tipo de documentos
TIPO_DOCUMENTO_CHOICES = (
    ("", '---------'),
    (1, 'CPF'),
    (2, 'CNPJ'),
)

class ProcedimentoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProcedimentoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Procedimento
        widgets = {
            'nome_parte': TextInput(attrs={'class': 'input-xxlarge'}),
            'email': TextInput(attrs={'class': 'input-xxlarge'}),
            'tipo_documento': Select(attrs={'class': 'input-small'}, choices=TIPO_DOCUMENTO_CHOICES),
            'tipo_documento_conteudo': TextInput(attrs={'class': 'input-medium'}),
            'observacoes': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xxlarge'})
        }

    def clean(self):
        cleaned_data = super(ProcedimentoForm, self).clean()
        tipo_documento = cleaned_data.get("tipo_documento")
        tipo_documento_conteudo = cleaned_data.get("tipo_documento_conteudo")

        if tipo_documento:
            if int(tipo_documento) == 1 and not tipo_documento_conteudo:
                raise forms.ValidationError("CPF inválido.")
            elif int(tipo_documento) == 2 and not tipo_documento_conteudo:
                raise forms.ValidationError("CNPJ inválido.")

        return self.cleaned_data


class ExigenciaForm(ModelForm):

    class Meta:
        model = Exigencia
        widgets = {
            'conteudo': AutosizedTextarea(attrs={'rows': 1, 'class': 'input-xxlarge'})
        }


class GrupoTrabalhoAuditorForm(ModelForm):

    class Meta:
        model = GrupoTrabalhoAuditor

    try:
        # Pega o objeto referente ao grupo de Auditores
        group = Group.objects.get(id=1)

        # Retorna a lista com os nomes dos membros do grupo
        auditor = UserModelGrupoChoiceField(group.user_set.all().order_by('usuario_inspetoria__inspetoria', 'first_name', 'last_name', 'username'))
    except:
        pass
