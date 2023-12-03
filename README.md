# Gerenciador-Escopo-Tipos

Repositório para a avaliação da disciplina de Compiladores. O trabalho se resume na criação de um gerenciador de escopo e verificação de tipos por meio de tabela de símbolos para uma linguagem fictícia simplificada com único propósito de permitir atribuições de valores e criação de escopo.

O projeto utiliza pilha de listas para gerenciar os escopos e as variáveis.

Desenvolvido por: [João Manoel](https://github.com/John-Parsec)


# Como Executar o Projeto

Para executar o projeto basta rodar o arquivo `main.py` na pasta _src_.
É possível passar o caminho para o arquivo do código a ser analisado como um parâmetro na execução do main.

Exemplos de uso:
```
python3 main.py
```

Ou 

```
python3 main.py caminho/para/arquivo.txt
```

Ao rodar sem passar o arquivo como parâmetro o programa solicitará o caminho no terminal.

A saída do programa será mostrada no terminal.



# Projeto


-  Palavras reservadas 'BLOCO', 'PRINT' e 'FIM'.
-   Tipos de dados: 'NUMERO' e 'CADEIA'.
-   Só é permitido fazer atribuições, declarações e exibir os valores de variáveis.

### Escopos

São adicionados a pilha com a palavra reservada BLOCO e removidos com a palavra reservada FIM

### Atribuição

É permitido atribui a uma variável já existente apenas valores condizentes com o tipo de dado da variável. Além de permitir atribuir a uma variável o valor de outra se a outra for do mesmo tipo de dado.
Além disso é permitido atribui um valor para uma variável direto na sua criação.

### Declaração
As declarações podem ser feitas através das palavras reservadas de tipo de dado, criando variáveis do tipo representado pela palavra. Por exemplo:
```
NUMERO a
CADEIA b
```
Também é permitido declaração de multiplas variaveis do mesmo tipo usando `,` após o identificador da variável, além de permitir já atribuir um valor na declaração.

Exemplo:
```
NUMERO num1 = 10, num2
CADEIA c = "Cadeia", d = "Teste"
```

Por fim, também é permito a declaração de uma variável não existente sem o uso de palavras reservadas ao atribuir um valor para ela, assim a variável é criada com o tipo de dado do valor atribuído.

Exemplo: 
```
var = 15
teste = "Hello World!"
```

### Print

A palavra reservada PRINT permite a exibição do valor de uma variável.
A exibição segue o padrão: `<variavel>: <valor>`

Exemplo:
```
PRINT a
```

# Exemplo

Na pasta _src_ possui um arquivo `exemplo.txt` que contem o código dado de exemplo para testar o programa, além de um arquivo `saida.png` sendo uma imagem com a saída esperada para o exemplo.

Para rodar diretamente o exemplo basta por no terminal :

```
python3 main.py exemplo.txt
```

A saída do exemplo será mostrada no terminal.