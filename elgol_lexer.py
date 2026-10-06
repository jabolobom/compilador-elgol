import re
from dataclasses import dataclass, field

import ply.lex as lex

reservadas = {
    'elgio': 'ELGIO',
    'DECIMAL': 'DECIMAL',
    '_Z_': 'ZERO',
    '_NEG_': 'NEG',
    'EXP': 'EXP',
    'RESTO': 'RESTO',
    'enquanto': 'ENQUANTO',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'para': 'PARA',
    'inicio': 'INICIO',
    'fim': 'FIM',
    'maior': 'MAIOR',
    'menor': 'MENOR',
    'igual': 'IGUAL',
    'diferente': 'DIFERENTE',
    'migual': 'MIGUAL_MIN',  
    'MIgual': 'MIGUAL_MAI',  
}

operadores_palavra = {
    'x': 'MULT',
}

tokens = [
    'ID',  # identificador
    'FUNCAO',  # nome de função
    'NUM',  # número inteiro
    'ATRIB',  # =
    'MAIS',  # +
    'MENOS',  # -
    'DIV',  # /
    'MULT',  # x
    'PONTO',  # .  fim
    'VIRGULA',  # ,  
    'ABRE_PAR',  # (
    'FECHA_PAR',  # )
] + list(reservadas.values())


LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
MAIUSCULAS = LETRAS[:26]
MINUSCULAS = LETRAS[26:]
VOGAIS_MAIUSCULAS = 'AEIOU'

RE_IDENTIFICADOR = re.compile(r'[B-DF-HJ-NP-TV-Z][A-Za-z]{2,}[a-z]')
# não começa com 0
RE_NUMERO = re.compile(r'[1-9][0-9]*')


@dataclass
class Simbolo:
    indice: int
    palavra: str
    categoria: str  # 'ID' ou 'FUNCAO'
    linha: int  # primeira ocorrência
    coluna: int
    ocorrencias: list = field(default_factory=list)  # [(linha, coluna), ...]


class TabelaSimbolos:
    def __init__(self):
        self._simbolos = {}  # palavra -> Simbolo (dict preserva a ordem de inserção)

    def registrar(self, palavra, categoria, linha, coluna):
        """Insere o símbolo (se novo), anota a ocorrência e devolve o índice."""
        simbolo = self._simbolos.get(palavra)
        if simbolo is None:
            simbolo = Simbolo(len(self._simbolos) + 1, palavra, categoria, linha, coluna)
            self._simbolos[palavra] = simbolo
        simbolo.ocorrencias.append((linha, coluna))
        return simbolo.indice

    def buscar(self, palavra):
        return self._simbolos.get(palavra)

    def __iter__(self):
        return iter(self._simbolos.values())

    def __len__(self):
        return len(self._simbolos)


@dataclass
class ErroLexico:
    linha: int
    coluna: int
    palavra: str
    mensagem: str

    def __str__(self):
        return f'linha {self.linha}, coluna {self.coluna}: {self.mensagem}'


def coluna(lexdata, lexpos):
    """Coluna (1-based) de uma posição absoluta do texto."""
    return lexpos - (lexdata.rfind('\n', 0, lexpos) + 1) + 1


def _lista(caracteres):
    # escapa caracteres
    return ', '.join(repr(c) for c in dict.fromkeys(caracteres))


def motivos_identificador(palavra):
    # regras que a palavra viola
    motivos = []
    primeiro = palavra[0]
    if primeiro not in MAIUSCULAS:
        motivos.append('não começa com letra maiúscula')
    elif primeiro in VOGAIS_MAIUSCULAS:
        motivos.append(f"começa com a vogal '{primeiro}' (deve começar com consoante maiúscula)")
    estranhos = [c for c in palavra if c not in LETRAS]
    if estranhos:
        motivos.append(f'contém caracteres que não são letras A-Z/a-z: {_lista(estranhos)}')
    if len(palavra) < 4:
        motivos.append(f'tem {len(palavra)} caractere(s); o mínimo é 4')
    if palavra[-1] not in MINUSCULAS:
        motivos.append('não termina com letra minúscula')
    return motivos


def motivos_numero(palavra):
    # regras de numero que a palavra viola
    motivos = []
    if palavra[0] == '0':
        if set(palavra) == {'0'}:
            motivos.append('o número zero não existe em Elgol; use o operador _Z_')
        else:
            motivos.append('número não pode começar com 0')
    estranhos = [c for c in palavra if c not in '0123456789']
    if estranhos:
        motivos.append(
            f'contém caracteres que não são dígitos 0-9: {_lista(estranhos)} '
            '(identificadores não começam com dígito; operadores como x, EXP e '
            'RESTO precisam de espaço: 3 x 4)'
        )
    return motivos


def _sugestao(palavra):
    # sugestao de palavra parecida
    parecidas = [p for p in (*reservadas, *operadores_palavra) if p.lower() == palavra.lower()]
    if not parecidas:
        return ''
    return f" (você quis dizer {' ou '.join(repr(p) for p in parecidas)}?)"


def _registrar_erro(t, mensagem):
    t.lexer.erros.append(
        ErroLexico(t.lineno, coluna(t.lexer.lexdata, t.lexpos), t.value, mensagem)
    )

t_ignore = ' \t\r '

t_ignore_COMENTARIO = r'\*[^\n]*'

t_ATRIB = r'='
t_MAIS = r'\+'
t_MENOS = r'-'
t_DIV = r'/'
t_PONTO = r'\.'
t_VIRGULA = r','
t_ABRE_PAR = r'\('
t_FECHA_PAR = r'\)'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_FUNCAO(t):
    r'\$\w*'
    nome = t.value[1:]
    if not nome:
        motivos = ["'$' sem nome de função"]
    elif nome in reservadas or nome in operadores_palavra:
        motivos = [f"'{nome}' é palavra reservada, não identificador"]
    else:
        motivos = [] if RE_IDENTIFICADOR.fullmatch(nome) else motivos_identificador(nome)
    if motivos:
        _registrar_erro(t, f"'{t.value}' não é um nome de função válido: {'; '.join(motivos)}")
        return None
    t.lexer.tabela.registrar(t.value, 'FUNCAO', t.lineno, coluna(t.lexer.lexdata, t.lexpos))
    return t


def t_NUM(t):
    r'\d\w*'
    if not RE_NUMERO.fullmatch(t.value):
        motivos = '; '.join(motivos_numero(t.value))
        _registrar_erro(t, f"'{t.value}' não é um número válido: {motivos}")
        return None
    return t


def t_ID(t):
    r'[^\W\d]\w*'
    # primeiro ve se é reservada
    if t.value in reservadas:
        t.type = reservadas[t.value]
        return t
    # se nao for ve se é operador
    if t.value in operadores_palavra:
        t.type = operadores_palavra[t.value]
        return t
    if not RE_IDENTIFICADOR.fullmatch(t.value):
        motivos = '; '.join(motivos_identificador(t.value)) + _sugestao(t.value)
        _registrar_erro(t, f"'{t.value}' não é um identificador válido: {motivos}")
        return None
    t.lexer.tabela.registrar(t.value, 'ID', t.lineno, coluna(t.lexer.lexdata, t.lexpos))
    return t


def t_error(t):
    c = t.value[0]
    t.value = c
    _registrar_erro(t, f'caractere inválido {c!r} (U+{ord(c):04X})') # essa loucura aqui aponta o codigo unicode do caractere U+ alguma coisa
    t.lexer.skip(1)


_lexer_base = lex.lex()


def criar_lexer():
    lexer = _lexer_base.clone()
    lexer.lineno = 1
    lexer.tabela = TabelaSimbolos()
    lexer.erros = []
    return lexer


@dataclass
class Token:
    tipo: str
    palavra: str
    linha: int
    coluna: int
    atributo: object = None 


@dataclass
class ResultadoLexico:
    tokens: list
    tabela: TabelaSimbolos
    erros: list

    @property
    def ok(self):
        return not self.erros


def analisar(codigo): 
    lexer = criar_lexer()
    lexer.input(codigo)
    lista = []
    for t in lexer:
        if t.type in ('ID', 'FUNCAO'):
            atributo = lexer.tabela.buscar(t.value).indice
        elif t.type == 'NUM':
            atributo = int(t.value)
        elif t.type == 'ZERO':
            atributo = 0
        else:
            atributo = None
        lista.append(Token(t.type, t.value, t.lineno, coluna(codigo, t.lexpos), atributo))
    return ResultadoLexico(lista, lexer.tabela, lexer.erros)
