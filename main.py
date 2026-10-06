import argparse
import sys
from pathlib import Path

from elgol_lexer import analisar

def ler_input(caminho):
    if caminho == '-':
        dados = sys.stdin.buffer.read() # le o stdin do terminal
    else:
        with open(caminho, 'rb') as arquivo:
            dados = arquivo.read() # le o arquivo de text
    return dados.decode('utf-8-sig') # decoda como unicode (com ou sem BOM)


def _formatar_tabela(cabecalho, linhas):
    larguras = [max(len(str(c)) for c in coluna) for coluna in zip(cabecalho, *linhas)]
    saida = []
    for linha in (cabecalho, *linhas):
        saida.append('  ' + '  '.join(str(c).ljust(w) for c, w in zip(linha, larguras)).rstrip())
    return '\n'.join(saida)


def _plural(n, palavra):
    return f"{n} {palavra}{'s' if n != 1 else ''}"


def _atributo(token):
    if token.tipo in ('ID', 'FUNCAO'):
        return f'símbolo {token.atributo}'
    if token.atributo is not None:
        return f'valor {token.atributo}'
    return ''


def relatoriotxt(nome, resultado):
    partes = ['resultado da analise do arquivo' f' {nome}:\n']
    partes.append(f'\nLISTA DE TOKENS ({len(resultado.tokens)})')
    linhas = [
        (i, f'{t.linha}:{t.coluna}', t.tipo, t.palavra, _atributo(t))
        for i, t in enumerate(resultado.tokens, 1)
    ]
    partes.append(_formatar_tabela(('#', 'LIN:COL', 'TOKEN', 'PALAVRA', 'ATRIBUTO'), linhas))

    partes.append(f'\nTABELA DE SÍMBOLOS ({len(resultado.tabela)})')
    linhas = [
        (
            s.indice,
            s.palavra,
            s.categoria,
            f'{s.linha}:{s.coluna}',
            len(s.ocorrencias),
            ', '.join(str(lin) for lin in dict.fromkeys(lin for lin, _ in s.ocorrencias)),
        )
        for s in resultado.tabela
    ]
    partes.append(
        _formatar_tabela(('ÍNDICE', 'PALAVRA', 'CATEGORIA', '1ª OCORR.', 'QTD', 'LINHAS'), linhas)
    )

    if resultado.erros:
        partes.append(f'\nERROS LÉXICOS ({len(resultado.erros)})')
        partes.extend(f'  {erro}' for erro in resultado.erros)

    n = len(resultado.erros)
    situacao = 'OK, nenhum erro léxico' if n == 0 else f"{n} {'erros léxicos' if n > 1 else 'erro léxico'}"
    partes.append(
        f'\nRESULTADO: {situacao} '
        f"({_plural(len(resultado.tokens), 'token')}, {_plural(len(resultado.tabela), 'símbolo')})\n"
    )
    return '\n'.join(partes)


def caminho_saida(caminho):
    # enunciado.elgol -> enunciado_saida.txt, na mesma pasta do arquivo de entrada
    if caminho == '-':
        return Path('saida.txt')
    entrada = Path(caminho)
    return entrada.with_name(entrada.stem + '_saida.txt')


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='main.py', description='Analisador léxico de ELGOL em PLY'
    )
    parser.add_argument('arquivos', nargs='+', metavar='ARQUIVO', help="código Elgol ('-' = stdin)")
    args = parser.parse_args(argv)

    codigo_saida = 0
    for caminho in args.arquivos:
        nome = '<stdin>' if caminho == '-' else caminho
        try:
            codigo = ler_input(caminho)
        except OSError as erro:
            print(f'main.py: não foi possível ler {nome}: {erro.strerror}', file=sys.stderr)
            codigo_saida = 2
            continue
        except UnicodeDecodeError:
            print(f'main.py: {nome} não está em UTF-8', file=sys.stderr)
            codigo_saida = 2
            continue

        resultado = analisar(codigo)
        if not resultado.ok and codigo_saida == 0:
            codigo_saida = 1

        relatorio = relatoriotxt(nome, resultado)
        print(relatorio)
        destino = caminho_saida(caminho)
        try:
            destino.write_text(relatorio + '\n', encoding='utf-8')
        except OSError as erro:
            print(f'main.py: não foi possível gravar {destino}: {erro.strerror}', file=sys.stderr)
            codigo_saida = 2

    return codigo_saida


if __name__ == '__main__':
    sys.exit(main())
