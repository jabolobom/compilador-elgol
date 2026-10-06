## Documentação das regras

[regras_lexicas.md](regras_lexicas.md)

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
# relatório completo: tokens, tabela de símbolos e erros
.venv/bin/python main.py enunciado.elgol

# vários arquivos de uma vez
.venv/bin/python main.py enunciado.elgol enunciado_arrumado.elgol

# arquivos que inclui pra testar
# enunciado_arrumado.elgol - o mesmo do enunciado só que sem o erro léxico
# fatorial.elgol - vai ter vários erros
# operacoes.elgol - não deve apresentar nenhum erro

# ler o código da entrada padrão
cat fatorial.elgol | .venv/bin/python main.py -
```

O relatório é mostrado no terminal e também gravado em um `.txt` na mesma pasta
do arquivo analisado (`nomearquivo-saida.txt`).

Se o `.txt` já existir, ele é sobrescrito.

Códigos de saída: `0` = nenhum erro léxico, `1` = há erros léxicos,
`2` = arquivo não pôde ser lido ou o `.txt` não pôde ser gravado.

Exemplo do output:

```
TABELA DE SÍMBOLOS (7)
  ÍNDICE  PALAVRA    CATEGORIA  1ª OCORR.  QTD  LINHAS
  1       $Soma      FUNCAO     5:9        2    5, 25
  2       Numm       ID         5:24       2    5, 7
  ...

ERROS LÉXICOS (1)
  linha 14, coluna 11: 'Vim' não é um identificador válido: tem 3 caractere(s); o mínimo é 4

RESULTADO: 1 erro léxico (75 tokens, 7 símbolos)
```
