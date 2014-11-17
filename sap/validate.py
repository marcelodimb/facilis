import re

class Validate:
    def __init__( self ):
        """
        Class para interagir com as validacoes dos formularios
        """
        pass

    # Validador de telefone fixo
    def validate_telefone_fixo(self, str):
        if len(str) != 14:
            return False

        return bool(re.match('\(\d{2}\) \d{4}-\d{4}', str))

    # Validador de telefone celular
    def validate_telefone_celular(self, str):
        if len(str) != 15:
            return False

        return bool(re.match('\(\d{2}\) \d{5}-\d{4}', str))

    # Validador de CPF
    def validate_cpf(self, cpf):
        cpf_invalidos = [11*str(i) for i in range(10)]

        if cpf:
            if not cpf.isdigit():
                # Verifica se o CPF contem pontos e hifens
                cpf = cpf.replace( ".", "" )
                cpf = cpf.replace( "-", "" )

            # Verifica se todos os digitos sao iguais
            if cpf in cpf_invalidos:
                return False

            if len(cpf) < 11:
                # Verifica se o CPF tem 11 digitos
                return False

            if len(cpf) > 11:
                # CPF tem que ter 11 digitos
                return False

            selfcpf = [int( x ) for x in cpf]
            cpf = selfcpf[:9]

            while len( cpf ) < 11:
                r =  sum([(len(cpf)+1-i)*v for i, v in [(x, cpf[x]) for x in range(len(cpf))]]) % 11

                if r > 1:
                    f = 11 - r
                else:
                    f = 0
                cpf.append(f)

            return bool(cpf == selfcpf)

        return False

    # Validador de CNPJ
    def validate_cnpj(self, cnpj):
        # defining some variables
        lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4 , 3, 2]
        lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # cleaning the cnpj
        cnpj = cnpj.replace("-", "")
        cnpj = cnpj.replace(".", "")
        cnpj = cnpj.replace("/", "")

        # finding out the digits
        verificadores = cnpj[-2:]

        # verifying the lenght of the cnpj
        if len(cnpj) != 14:
            return False

        # calculating the first digit
        soma = 0
        id = 0
        for numero in cnpj:
            # to do not raise indexerrors
            try:
                lista_validacao_um[id]
            except:
                break

            soma += int(numero) * int(lista_validacao_um[id])
            id += 1

        soma = soma % 11
        if soma < 2:
            digito_um = 0
        else:
            digito_um = 11 - soma

        digito_um = str(digito_um) # converting to string, for later comparison

        # calculating the second digit
        # suming the two lists
        soma = 0
        id = 0

        # suming the two lists
        for numero in cnpj:
            # to do not raise indexerrors
            try:
                lista_validacao_dois[id]
            except:
                break

            soma += int(numero) * int(lista_validacao_dois[id])
            id += 1

        # defining the digit
        soma = soma % 11
        if soma < 2:
            digito_dois = 0
        else:
            digito_dois = 11 - soma

        digito_dois = str(digito_dois)

        # returnig
        return bool(verificadores == digito_um + digito_dois)
