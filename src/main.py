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

    words = getWords(file_path)
    
    for word in words:
        print(word)

    print("\n\n")

    i = 0

    while i < len(words):
        if words[i] == "BLOCO":
            if isBlock(words[i+1]):
                i += 1
                escopo = []
                pilha.append(escopo)
            else:
                print("ERRO: Bloco inválido")

        elif words[i] == "NUMERO":
            while True:
                i += 1
                try:
                    if isIdentifier(words[i]):
                        var = words[i]

                        if words[i+1] == "=":
                            i += 2
                            if isNumber(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': "NUMERO", 'valor': words[i]})
                                
                            else:
                                print("ERRO: Número inválido")
                        else:
                            pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': "NUMERO", 'valor': None})

                    else:
                        print("ERRO: Identificador inválido")
                    
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
                        var = words[i]

                        if words[i+1] == "=":
                            i += 2
                            if isString(words[i]):
                                pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': "CADEIA",'valor': words[i]})
                                
                            else:
                                print("ERRO: Cadeia inválida")
                        else:
                            pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': "CADEIA", 'valor': None})

                    else:
                        print("ERRO: Identificador inválido")
                    
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
                        print(dic['lexema'], " = " , dic['valor'])
                        flag = False
                        break
                
                cont -= 1
            
            if flag:
                print("ERRO: Variável não declarada")
            

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
                if(words[i+1] == "="):
                    i += 2
                    if isNumber(words[i]):
                        pilha[-1].append({'token': 'tk_identificador','lexema': words[i-1],'tipo': "NUMERO",'valor': words[i]})
                    elif isString(words[i]):
                        pilha[-1].append({'token': 'tk_identificador','lexema': words[i-1],'tipo': "CADEIA",'valor': words[i]})
                    else:
                        print("ERRO: Valor inválido")
                else:
                    print("ERRO: Variável não declarada: " + words[i])

            else:
                tipo = var['tipo']

                try:
                    if words[i+1] == "=":
                        i += 2

                        if tipo == "NUMERO":
                            if isNumber(words[i]):
                                var['valor'] = words[i]
                            else:
                                print("ERRO: Número inválido")
                        elif tipo == "CADEIA":
                            if isString(words[i]):
                                var['valor'] = words[i]
                            else:
                                print("ERRO: Cadeia inválida")
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

    words = re.findall(r'\b\w+\b|[=,]|"[^"]*"', content)

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