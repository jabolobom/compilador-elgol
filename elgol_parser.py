import ply.yacc
from elgol_lexer import criar_lexer, tokens

start = 'programa'
### GRAMATICA
### ###
def p_fim_cmd(p): 'fim_cmd : PONTO NL'

def p_valor(p): # os pipes | indicam a possibilidade, tem que ser em newline se nao ele surta
    '''valor : ID
             | NUM
             | ZERO'''

def p_op_mat(p): # operacao mat
    '''op_mat : MAIS
              | MENOS
              | MULT
              | DIV
              | EXP
              | RESTO'''

def p_op_rel(p): # operacao relacao, "if"
    '''op_rel : MAIOR
              | MENOR
              | IGUAL
              | DIFERENTE
              | MIGUAL_MAI
              | MIGUAL_MIN'''

def p_vazio(p): 'vazio : '

def p_operando(p):
    '''operando : valor
                | chamada'''

def p_expressao(p):
    '''expressao : expressao op_mat operando
                 | operando'''

def p_chamada(p): 'chamada : FUNCAO ABRE_PAR argumentos FECHA_PAR'
# veja que argumentos é definido dps de chamada, nao importa, o ply le tudo antes e constroi a gramatica
def p_argumentos(p):
    '''argumentos : argumentos VIRGULA valor
                  | valor'''

def p_expressao_simples(p): # palavra reservada elgio
    '''expressao_simples : expressao_simples op_mat valor
                         | valor'''

# comandos, declaracao atrib, retorno, negar, condicional, while
def p_declaracao(p): 'declaracao : DECIMAL ID fim_cmd'

def p_atribuicao(p): 'atribuicao : ID ATRIB expressao fim_cmd'

def p_retorno(p): 'retorno : ELGIO ATRIB expressao_simples fim_cmd'

def p_negacao(p): 'negacao : NEG ID fim_cmd'

def p_condicao(p): 'condicao : valor op_rel valor'

# blocos, if while funcao e zas e zas
def p_bloco(p): 'bloco : INICIO fim_cmd comandos FIM fim_cmd'

def p_comandos(p):
    '''comandos : comandos comando
                | vazio'''

def p_comando(p):
    '''comando : declaracao
               | atribuicao
               | retorno
               | negacao
               | se
               | enquanto
               | para'''

def p_comando_erro(p): # erro numa linha: pula ate o fim da linha (NL) e continua
    'comando : error NL'
    p.parser.errok()

def p_se(p): 'se : SE condicao fim_cmd ENTAO fim_cmd bloco SENAO fim_cmd bloco'

def p_enquanto(p): 'enquanto : ENQUANTO condicao fim_cmd bloco'

def p_para(p): 'para : PARA ID valor fim_cmd bloco'

# programa, funcoes, parametros
def p_programa(p): 'programa : nl_opt funcoes bloco'

def p_nl_opt(p): # newline opcional, tem prgroama q começa com comment q fica como nl
    '''nl_opt : NL
              | vazio''' # cairia como erro de sintaxe na linha 1 se nao tivesse isso

def p_funcoes(p):
    '''funcoes : funcoes funcao
               | vazio'''

def p_funcao(p): 'funcao : DECIMAL FUNCAO ABRE_PAR parametros FECHA_PAR fim_cmd bloco'

def p_parametros(p):
    '''parametros : parametros VIRGULA parametro
                  | parametro'''

def p_parametro(p): 'parametro : DECIMAL ID'

erros_sintaticos = []

def p_error(t): 
    if t is None: e = (None, 'fim do arquivo');
    elif t.type == 'NL': e = (t.lineno, 'fim da linha'); 
    else: e = (t.lineno, t.value)

    return erros_sintaticos.append(e);

parser = ply.yacc.yacc(debug=True)

def analise_sintaxe(codigo):
    erros_sintaticos.clear()
    lexer = criar_lexer()
    lexer.input(codigo + '\n')
    parser.parse(lexer=lexer)

    resultado = []
    for linha, palavra in erros_sintaticos:
        if linha is None:
            linha = codigo.count('\n') + 1
        resultado.append((linha, palavra))
    return resultado
    