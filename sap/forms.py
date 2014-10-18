from django.forms import ModelForm, TextInput
from .models import Procedimento, Exigencia
from suit.widgets import AutosizedTextarea

class ProcedimentoForm(ModelForm):

    class Meta:
        model = Procedimento
        widgets = {
            'interessado': TextInput(attrs={'class': 'input-xxlarge'}),
            'email': TextInput(attrs={'class': 'input-xxlarge'}),
            'observacoes': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xxlarge'})
        }


class ExigenciaForm(ModelForm):

    class Meta:
        model = Exigencia
        widgets = {
            'conteudo': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xxlarge'})
        }
