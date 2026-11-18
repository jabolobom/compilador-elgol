## Documentação das regras

[regras_lexicas.md](regras_lexicas.md)

[regras_sintaticas.md](regras_sintaticas.md)

## Requisitos

- Python 3
- PLY 3.11

## Instalação

```bash
cd "compilador-elgol-main"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

No Windows (PowerShell):

```powershell
cd "compilador-elgol-main"
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Uso

(Executar dentro do venv)

```bash
# relatório completo: tokens, tabela de símbolos, erros léxicos e sintáticos
.venv/bin/python main.py enunciado.elgol

# vários arquivos de uma vez
.venv/bin/python main.py enunciado.elgol enunciado_arrumado.elgol

# arquivos que inclui pra testar
# enunciado_arrumado.elgol - o mesmo do enunciado só que sem os erros léxicos (ainda tem 1 erro sintático: falta o senao)
# fatorial.elgol - vai ter vários erros
# operacoes.elgol - não deve apresentar nenhum erro
# exemplo1.elgol ... exemplo5.elgol - exemplos do enunciado da etapa 2 (só o exemplo1 não tem erros)

# ler o código da entrada padrão
cat fatorial.elgol | .venv/bin/python main.py -
```

O relatório é mostrado no terminal e também gravado em um `.txt` na mesma pasta
do arquivo analisado (`nomearquivo_saida.txt`).

Se o `.txt` já existir, ele é sobrescrito.

Códigos de saída: `0` = nenhum erro, `1` = há erros léxicos ou sintáticos,
`2` = arquivo não pôde ser lido ou o `.txt` não pôde ser gravado.

Na execução o PLY gera `parsetab.py` e `parser.out` (estados e conflitos da gramática) na pasta do
projeto. Os dois estão no `.gitignore`.

Exemplo do output:

```
TABELA DE SÍMBOLOS (7)
  ÍNDICE  PALAVRA    CATEGORIA  1ª OCORR.  QTD  LINHAS
  1       Numm       ID         5:25       2    5, 7
  2       Dois       ID         5:39       1    5
  ...

ERROS LÉXICOS (3)
  linha 5, coluna 9: '$Soma3' não é um nome de função válido: contém caracteres que não são letras A-Z/a-z: '3'; não termina com letra minúscula
  linha 14, coluna 11: 'Vim' não é um identificador válido: tem 3 caractere(s); o mínimo é 4
  linha 23, coluna 23: '04' não é um número válido: número não pode começar com 0

ERROS SINTÁTICOS (4)
  linha 5: erro de sintaxe próximo de '('
  linha 11: erro de sintaxe próximo de 'inicio'
  linha 23: erro de sintaxe próximo de '.'
  linha 27: erro de sintaxe próximo de 'fim'

RESULTADO: 3 erros léxicos, 4 erros sintáticos (73 tokens, 7 símbolos)
```
