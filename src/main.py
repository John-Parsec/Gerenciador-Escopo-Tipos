import re
import sys

def main(argv, argc):
    if argc > 1:
        file_path = argv[1]        
    else:
        file_path = input("Digite o caminho do arquivo: ")
    
    gerenciador(file_path)

def gerenciador(file_path: str):
    """
    Função que gerencia as variaveis e escopos do programa.
    Valida as variaveis e exibe o valor referente quando solicitado no codigo lido.
    Exibe as mensagens de erro quando necessário.

    Recebe como parametro o caminho do arquivo. (string)
    """
    pilha = []
    i = 0
    words = getWords(file_path)

    while i < len(words):                   # Percorre todas as palavras do arquivo
        if words[i] == "BLOCO":             # Se a palavra for BLOCO, tenta criar um novo escopo
            try:
                if isBlock(words[i+1]):
                    i += 1
                    escopo = []
                    pilha.append(escopo)    # Adiciona o escopo na pilha
                else:
                    print("ERRO: nome de bloco inválido")
            except:                                         # Se não tiver proxima palavra, chegou no fim do arquivo 
                print("ERRO: bloco sem nome")   

        elif words[i] == "NUMERO":          # Se a palavra for NUMERO, tenta criar uma variavel do tipo NUMERO
            while True:                     
                i += 1
                try:
                    if isIdentifier(words[i]):         
                        if(verifyVarInScope(words[i], pilha)):      # Verifica se a variavel já existe no escopo atual
                            print("ERRO: Variável já declarada!")
                            break

                        var = words[i]                  # Salva o lexema do identificador

                        if words[i+1] == "=":           # Se a proxima palavra for um =, tenta atribuir um valor a variavel
                            i += 2
                            if isNumber(words[i]):      
                                pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': "NUMERO", 'valor': words[i]})
                                
                            else:
                                print("ERRO: Número mal formatado!")

                        else:
                            pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': "NUMERO", 'valor': None})

                    else:
                        print("ERRO: Identificador mal formatado!")
                    
                    if words[i+1] != ',':       # Se a proxima palavra for virgula, continua lendo a linha
                        break
                    else:
                        i += 1
                except:            # Se não tiver proximo lexema, chegou no fim do arquivo
                    break

        elif words[i] == "CADEIA":      # Se a palavra for CADEIA, tenta criar uma variavel do tipo CADEIA
            while True:                 
                i += 1
                try:
                    if isIdentifier(words[i]):                      
                        if(verifyVarInScope(words[i], pilha)):      # Verifica se a variavel já existe no escopo atual
                            print("ERRO: Variável já declarada!")
                            break

                        var = words[i]

                        if words[i+1] == "=":           # Se a proxima palavra for um =, tenta atribuir um valor a variavel
                            i += 2
                            if isString(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': "CADEIA",'valor': words[i]})
                                
                            else:
                                print("ERRO: Cadeia mal formatada!")
                        else:
                            pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': "CADEIA", 'valor': None})

                    else:
                        print("ERRO: Identificador mal formatado!")
                    
                    if words[i+1] != ',':       # Se a proxima palavra for virgula, continua lendo a linha
                        break
                    else:
                        i += 1

                except:       # Se não tiver proxima palavra, chegou no fim do arquivo
                    break

        elif words[i] == "PRINT":           # Se a palavra for PRINT, tenta exibir o valor da variavel
            cont = len(pilha) - 1
            flag = True
            i += 1

            while cont >= 0 and flag:       # Percorre a pilha de escopos a partir do topo até encontrar a variavel
                topo = pilha[cont]

                for dic in topo:
                    if words[i] == dic['lexema']:       # Se achar a variavel, exibe o valor e sai do loop
                        print(dic['lexema'], ": " , dic['valor'])
                        flag = False
                        break
                
                cont -= 1
            
            if flag:        # Se não achar a variavel, exibe mensagem de erro
                print("ERRO: Não é possivel exibir variavel não declarada! ( " + words[i] + " )")

        elif words[i] == "FIM":         # Se a palavra for FIM, remover o escopo atual da pilha
            i += 1
            if len(pilha) > 0:
                pilha.pop()             
            else:
                print("ERRO: Fim sem bloco")
                break

        elif isIdentifier(words[i]):            
            var = getVar(words[i], pilha)       # Verifica se a variavel já existe na pilha, se existir, retorna o dicionario com as informações da variavel

            if var == None:                     # Se a variavel não existir na pilha, tenta criar uma nova variavel
                try:
                    if(words[i+1] == "="):              # Se a proxima palavra for um =, tenta atribuir um valor a variavel
                        
                        var2 = getVar(words[i+2], pilha)        # Verifica se está atribuindo o valor de uma variavel existente

                        if var2 != None:                        
                            pilha[-1].append({'token': 'tk_identificador','lexema': words[i],'tipo': var2['tipo'],'valor': var2['valor']})

                        else:                                   
                            i += 2
                            if isNumber(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': words[i-2],'tipo': "NUMERO",'valor': words[i]})

                            elif isString(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': words[i-2],'tipo': "CADEIA",'valor': words[i]})

                            else:
                                print("ERRO: Tipo inexistente!")
                    else:
                        print("ERRO: Declaração inválida! (" + words[i] + ")")
                except:
                    pass

            else:                           # Se a variavel existir na pilha, tenta atribuir um valor a ela
                tipo = var['tipo']          

                try:
                    if words[i+1] == "=":
                        i += 2

                        var2 = getVar(words[i], pilha)      # Verifica se está atribuindo o valor de uma variavel existente, se sim, pega os dados da variavel

                        if var2 != None:
                            if var2['tipo'] == tipo:        # Se a variavel existir na pilha e for do mesmo tipo, atribui o valor da variavel
                                var['valor'] = var2['valor']

                            else:
                                print("ERRO: Não é possivel atribuir! Tipos incompatíveis!")

                        else:                                   # Se não for uma variavel, trata como uma atribuição normal
                            if tipo == "NUMERO":                # Se a variavel for do tipo NUMERO, tenta atribuir um valor do tipo NUMERO
                                if isNumber(words[i]):
                                    var['valor'] = words[i]

                                else:
                                    print("ERRO: Número mal formatado!")

                            elif tipo == "CADEIA":              # Se a variavel for do tipo CADEIA, tenta atribuir um valor do tipo CADEIA
                                if isString(words[i]):
                                    var['valor'] = words[i]

                                else:
                                    print("ERRO: Cadeia mal formatada!")
                except:
                    pass
            
        i += 1

def getWords(file_path: str) -> list:
    """
    Função que retorna uma lista de todas as palavras do arquivo, considerando também numeros(inteiros e reais), 
    qualquer cadeia entre aspas duplas(incluindo as aspas), virgulas e igual  como palavras completas.

    Recebe como parametro o caminho do arquivo. (string)
    Retorna uma lista de strings.
    """

    words = []

    word = ""
    with open(file_path, 'r') as f:
        while True:
            char = f.read(1)        # Lê um caracter do arquivo

            if not char:            # Se o caracter for vazio, chegou ao fim do arquivo
                break

            if char == " " or char == "\n":     # Se o caracter for espaço ou quebra de linha, chegou ao fim da palavra
                if word != "":
                    words.append(word)
                    word = ""

            elif char == "=" or char == ",":    # Se o caracter for igual ou virgula, chegou ao fim da palavra
                if word != "":          # Se a palavra não for vazia, adiciona na lista
                    words.append(word)
                    word = ""
                words.append(char)      # Adiciona o caracter na lista

            elif char == '"':           # Se o caracter for aspas duplas, chegou ao fim da palavra
                if word != "":          # Se a palavra não for vazia, adiciona na lista
                    words.append(word)
                    word = ""
                word += char            # Começa a cadeia com aspas duplas
                while True:             # Enquanto não chegar no fim da cadeia
                    char = f.read(1)
                    word += char
                    if char == '"':     # Se o caracter for aspas duplas, chegou no fim da cadeia
                        break
                words.append(word)
                word = ""

            else:
                word += char

    return words

def getVar(lexema: str, pilha: list) -> dict:
    """
    Função que retorna um dicionario com as informações da variavel, caso ela exista na pilha. (Considera sempre o escopo mais proximo)

    Recebe como parametro uma sitrng, sendo o lexema da variavel, e uma lista, sendo a pilha de escopos. (string, list)
    Retorna um dicionario com as informações da variavel ou None caso ela não exista. (dict)
    """
    cont = len(pilha) - 1

    while cont >= 0:
        topo = pilha[cont]

        for dic in topo:
            if lexema == dic['lexema']:
                return dic
        
        cont -= 1
    
    return None
    
def verifyVarInScope(lexema: str, pilha: list) -> bool:
    """
    Função que verifica se a variavel existe no escopo atual.

    Recebe como parametro uma sitrng, sendo o lexema da variavel, e uma lista, sendo a pilha de escopos. (string, list)
    Retorna True caso a variavel exista no escopo atual e False caso ela não exista. (bool)
    """
    topo = pilha[-1]

    for dic in topo:
        if lexema == dic['lexema']:
            return True
    
    return False

def isIdentifier(lexema: str) -> bool:
    """Função que verifica se o lexema é um identificador válido."""
    return bool(re.match(r'^[a-zA-Z][a-zA-Z_]*$', lexema))

def isNumber(lexema: str) -> bool:
    """Função que verifica se o lexema é um número válido."""
    return bool(re.match(r'[+-]?\d+(\.\d+)?', lexema))

def isString(lexema: str) -> bool:
    """Função que verifica se o lexema é uma cadeia de caracteres entre aspas."""
    return bool(re.match(r'"[^"]*"', lexema))

def isBlock(lexema: str) -> bool:
    """Função que verifica se o lexema é um nome de bloco válido."""
    return bool(re.match(r'^_[a-zA-Z0-9]+_$', lexema))


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))