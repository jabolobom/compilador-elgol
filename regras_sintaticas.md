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
