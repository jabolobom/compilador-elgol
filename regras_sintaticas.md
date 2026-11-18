Todas as regras estão em elgol_parser.py. Cada função `p_` tem a regra na docstring; o PLY lê todas antes de montar a gramática, então a ordem das funções não importa. As alternativas (`|`) precisam começar uma linha nova na docstring, senão o PLY dá `Illegal name '|'`.

**Fim de comando**: todo comando termina com `fim_cmd : PONTO NL`. O `NL` vem do léxico (`t_NL`), então "sempre termina com `.`" e "um comando por linha" já estão na gramática. Um `.` faltando é apontado na linha certa. Como o arquivo pode começar com comentários (que viram um `NL`), o `programa` começa com `nl_opt`. O código é analisado com um `\n` a mais no fim, pra última linha também terminar em `NL`.

## Gramática

```
programa          : nl_opt funcoes bloco
nl_opt            : NL | vazio
funcoes           : funcoes funcao | vazio
funcao            : DECIMAL FUNCAO ABRE_PAR parametros FECHA_PAR fim_cmd bloco
parametros        : parametros VIRGULA parametro | parametro
parametro         : DECIMAL ID

bloco             : INICIO fim_cmd comandos FIM fim_cmd
comandos          : comandos comando | vazio
comando           : declaracao | atribuicao | retorno | negacao | se | enquanto | para
                  | error NL

declaracao        : DECIMAL ID fim_cmd
atribuicao        : ID ATRIB expressao fim_cmd
retorno           : ELGIO ATRIB expressao_simples fim_cmd
negacao           : NEG ID fim_cmd

se                : SE condicao fim_cmd ENTAO fim_cmd bloco SENAO fim_cmd bloco
enquanto          : ENQUANTO condicao fim_cmd bloco
para              : PARA ID valor fim_cmd bloco

expressao         : expressao op_mat operando | operando
operando          : valor | chamada
expressao_simples : expressao_simples op_mat valor | valor
chamada           : FUNCAO ABRE_PAR argumentos FECHA_PAR
argumentos        : argumentos VIRGULA valor | valor
condicao          : valor op_rel valor
valor             : ID | NUM | ZERO
op_mat            : MAIS | MENOS | MULT | DIV | EXP | RESTO
op_rel            : MAIOR | MENOR | IGUAL | DIFERENTE | MIGUAL_MAI | MIGUAL_MIN
fim_cmd           : PONTO NL
```

Os pares plural/singular (`funcoes`/`funcao`, `comandos`/`comando`, `parametros`/`parametro`) são listas: a gramática não tem "repetir", então a lista é recursiva.

## Regras do enunciado na gramática

- **Sem precedência**: `expressao : expressao op_mat operando` é recursiva à esquerda, então a expressão é lida da esquerda pra direita (`Bare + Breca x _Z_` = `(Bare + Breca) x _Z_`). Não tem tabela `precedence` e a gramática não tem conflitos.
- **Função não pode ser alvo**: `atribuicao` começa com `ID`, nunca com `FUNCAO`.
- **`elgio` sem função**: `retorno` usa `expressao_simples`, que só aceita `valor` (sem `chamada`).
- **Função não pode ser parâmetro de função**: `argumentos` só aceita `valor` (`ID`, `NUM` ou `_Z_`).
- **Expressão lógica**: `condicao` tem exatamente 2 operandos (`valor`) e um `op_rel`. Operador matemático, função ou um terceiro operando é erro.
- **`se` sempre com `senao`**, mesmo vazio (bloco sem comandos).
- **`para`**: identificador contador e limite (`NUM`, `ID` ou `_Z_`).
- **Funções** vêm antes do bloco principal (`inicio . ... fim .`), que é obrigatório.
- `elgio` fora de função, variável/função não declarada e recursão são erros **semânticos** e não são verificados.

## Erros sintáticos

**p_error**: registra a linha e a palavra onde o parser travou. Se o token é `NL`, a linha acabou antes da hora (palavra `fim da linha`). Se não tem token, o arquivo acabou antes da hora (`fim do arquivo`, linha = última linha).

**comando : error NL**: recuperação de erro. Quando um comando dá erro, o parser descarta tokens até o fim da linha e continua (`p.parser.errok()` libera o próximo erro pra ser reportado na hora). Assim o relatório mostra vários erros, não só o primeiro.

Limitação: só existe ponto de recuperação dentro de blocos. Um erro no cabeçalho de uma função faz o parser perder alguns erros seguintes (no exemplo3, as linhas 3, 6 e 7 não aparecem depois do erro da linha 2). Todas as linhas reportadas têm erro de verdade.

Erros léxicos não param a análise: a palavra inválida é descartada e o parser continua com o resto, então uma linha com erro léxico normalmente também tem erro sintático.

## Resultado nos exemplos

| Arquivo | Erros léxicos (linha) | Erros sintáticos (linha) |
|---|---|---|
| exemplo1.elgol | - | - |
| exemplo2.elgol | 2, 2, 4, 5, 5, 6 | 2, 4, 5, 6 |
| exemplo3.elgol | - | 2, 11, 21, 25 |
| exemplo4.elgol | 20 | 17, 20 |
| exemplo5.elgol | 18, 21 | 5, 18, 22, 27 |
| enunciado.elgol | 5, 14, 23 | 5, 11, 23, 27 |
| enunciado_arrumado.elgol | - | 27 (falta o `senao`) |
| operacoes.elgol | - | - |
