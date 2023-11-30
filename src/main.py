import re
import sys

def main(argv, argc):
    if argc > 1:
        file_path = argv[1]        
    else:
        file_path = input("Digite o caminho do arquivo: ")
    
    gerenciador(file_path)

def gerenciador(file_path):
    pilha = []

    words = getWords2(file_path)
    
    # for word in words:
    #     print(word)

    # print("\n\n")

    i = 0

    while i < len(words):
        if words[i] == "BLOCO":
            if isBlock(words[i+1]):
                print()
                i += 1
                escopo = []
                pilha.append(escopo)
            else:
                print("ERRO: nome de bloco inválido")

        elif words[i] == "NUMERO":
            while True:
                i += 1
                try:
                    if isIdentifier(words[i]):
                        if(verifyVarInScope(words[i], pilha)):
                            print("ERRO: Variável já declarada!")
                            break

                        var = words[i]

                        if words[i+1] == "=":
                            i += 2
                            if isNumber(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': "NUMERO", 'valor': words[i]})
                                
                            else:
                                print("ERRO: Número mal formatado!")
                        else:
                            pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': "NUMERO", 'valor': None})

                    else:
                        print("ERRO: Identificador mal formatado!")
                    
                    if words[i+1] != ',':
                        break
                    else:
                        i += 1
                except:
                    break

        elif words[i] == "CADEIA":
            while True:
                i += 1
                try:
                    if isIdentifier(words[i]):
                        if(verifyVarInScope(words[i], pilha)):
                            print("ERRO: Variável já declarada!")
                            break

                        var = words[i]

                        if words[i+1] == "=":
                            i += 2
                            if isString(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': "CADEIA",'valor': words[i]})
                                
                            else:
                                print("ERRO: Cadeia mal formatada!")
                        else:
                            pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': "CADEIA", 'valor': None})

                    else:
                        print("ERRO: Identificador mal formatado!")
                    
                    if words[i+1] != ',':
                        break
                    else:
                        i += 1
                except:
                    break

        elif words[i] == "PRINT":
            cont = len(pilha) - 1
            flag = True

            while cont >= 0 and flag:
                topo = pilha[cont]

                for dic in topo:
                    if words[i+1] == dic['lexema']:
                        print(dic['lexema'], ": " , dic['valor'])
                        flag = False
                        break
                
                cont -= 1
            
            if flag:
                print("ERRO: Não é possivel exibir valor de variavel não declarada! ( " + words[i+1] + " )")

            i += 1
            

        elif words[i] == "FIM":
            i += 1
            if len(pilha) > 0:
                pilha.pop()
            else:
                print("ERRO: Fim sem bloco")
                break

        elif isIdentifier(words[i]):
            var = getVar(words[i], pilha)

            if var == None:
                try:
                    if(words[i+1] == "="):
                        
                        var2 = getVar(words[i+2], pilha)

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

            else:
                tipo = var['tipo']

                try:
                    if words[i+1] == "=":
                        i += 2

                        var2 = getVar(words[i], pilha)

                        if var2 != None:
                            if var2['tipo'] == tipo:
                                var['valor'] = var2['valor']
                                #pilha[-1].append({'token': 'tk_identificador','lexema': var['lexema'],'tipo': tipo,'valor': var2['valor']}) #testar
                            else:
                                print("ERRO: Tipos incompatíveis!")
                        else:
                            if tipo == "NUMERO":
                                if isNumber(words[i]):
                                    var['valor'] = words[i]
                                    #pilha[-1].append({'token': 'tk_identificador','lexema': var['lexema'],'tipo': "NUMERO",'valor': words[i]}) #testar
                                else:
                                    print("ERRO: Número mal formatado!")
                            elif tipo == "CADEIA":
                                if isString(words[i]):
                                    var['valor'] = words[i]
                                    #pilha[-1].append({'token': 'tk_identificador','lexema': var['lexema'],'tipo': "CADEIA",'valor': words[i]}) #testar
                                else:
                                    print("ERRO: Cadeia mal formatada!")
                except:
                    pass
            


        i += 1

    # for escopo in pilha:
    #     print("Escopo:")
    #     for var in escopo:
    #         print(var)
    #     print("")
        
        
        
def getWords(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # words = re.findall(r'\b\w+\b|[=,]|"[^"]*"', content) 

    words = re.findall(r'\b\w+\b|[=,]|"[^"]*"', content)
    
    return words


def getWords2(file_path):
    words = []

    word = ""
    with open(file_path, 'r') as f:
        while True:
            char = f.read(1)

            if not char:
                break

            if char == " " or char == "\n":
                if word != "":
                    words.append(word)
                    word = ""
            elif char == "=" or char == ",":
                if word != "":
                    words.append(word)
                    word = ""
                words.append(char)
            elif char == '"':
                if word != "":
                    words.append(word)
                    word = ""
                word += char
                while True:
                    char = f.read(1)
                    word += char
                    if char == '"':
                        break
                words.append(word)
                word = ""
            else:
                word += char

    return words


def getVar(lexema, pilha):
    cont = len(pilha) - 1
    flag = True

    while cont >= 0 and flag:
        topo = pilha[cont]

        for dic in topo:
            if lexema == dic['lexema']:
                return dic
        
        cont -= 1
    
    if flag:
        return None
    
def verifyVarInScope(lexema, pilha):
    topo = pilha[-1]

    for dic in topo:
        if lexema == dic['lexema']:
            return True
    
    return False



def isReservedWord(lexema):
    return lexema in ["BLOCO", "CADEIA", "PRINT", "FIM"]

def isIdentifier(lexema):
    return re.match(r'^[a-zA-Z][a-zA-Z_]*$', lexema)

def isNumber(lexema):
    return re.match(r'[+-]?\d+(\.\d+)?', lexema)

def isString(lexema):
    return re.match(r'"[^"]*"', lexema)

def isBlock(lexema):
    return re.match(r'^_[a-zA-Z0-9]+_$', lexema)


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))