from django.contrib.auth.models import Group, User
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from sap.models import GrupoTrabalho, GrupoTrabalhoAuditor, Procedimento

@csrf_exempt
def set_auditor_responsavel(request):
    """
    Funcao que define o auditor responsavel de acordo com o assunto solicitado.
    """
    output = ''

    if request.is_ajax() and request.method == 'POST':
        assunto_id = int(request.POST['assunto_id'])

        # Verifica se o assunto solicitado possui um grupo de trabalho associado e retorna o
        # auditor responsavel ou a lista contendo todos os auditores da inspetoria do usuario
        try:
            # Recupera o grupo de trabalho de acordo com o assunto informado
            gp = GrupoTrabalho.objects.get(assunto=assunto_id)

            # Recupera a lista de auditores presentes no grupo de trabalho encontrado
            gpt = GrupoTrabalhoAuditor.objects.filter(grupo_trabalho=gp)

            list_p = []

            for g in gpt:
                u = User.objects.get(username=g)
                p = Procedimento.objects.filter(auditor_responsavel=u)

                # Cria uma lista contendo o auditor e a quantidade de procedimentos recebidos por ele
                list_p.append((p.count(), u))

            # Define como auditor responsavel aquele que tiver o menor numero de procedimentos recebidos
            idx, val = min((val, idx) for (idx, val) in enumerate(list_p))
            auditor_responsavel = idx[1]
            output += '<option value="%s">%s</option>' % (auditor_responsavel.id, auditor_responsavel.get_full_name())
        except:
            user = User.objects.get(username=request.user.username)
            inspetoria = user.usuario_inspetoria.inspetoria

            # Pega o objeto referente ao grupo de Auditores(id=1)
            group = Group.objects.get(id=1)

            # Retorna a lista com os nomes dos membros do grupo
            auditores = group.user_set.all().filter(usuario_inspetoria__inspetoria=inspetoria.id).order_by('first_name', 'last_name', 'username')

            output = '<option value="" selected="selected">---------</option>'

            for a in auditores:
                output += '<option value="%s">%s</option>' % (a.id, a.get_full_name())
            pass
    else:
        raise Http404

    return HttpResponse(output)
