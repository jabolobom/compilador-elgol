Todas as regras estão em elgol_lexer.py. As regras de palavra (**t_ID**, **t_FUNCAO**, **t_NUM**) capturam a palavra inteira e só depois validam.

**t_ID**: palavra que começa com letra ou `_`. Se estiver em `reservadas` (linha 6) vira o token da reservada. 
Se for `x` vira MULT (`operadores_palavra`). 
Senão precisa casar com `RE_IDENTIFICADOR`: consoante maiúscula, só letras, mínimo 4 caracteres, termina em minúscula. Se for válido vira ID e entra na tabela de símbolos. Se for inválido gera um erro e escolhe o motivo atraves do `motivos_identificador` e sugestão de reservada (`_sugestao`, linha 148).

**t_FUNCAO**: `$` seguido de um nome que segue a regra de identificador e não é reservada. Válido retorna token de função

**t_NUM**: palavra que começa com dígito. Precisa casar com `RE_NUMERO` (linha 55): inteiro que não começa com 0. O zero é escrito `_Z_`. Motivos do erro em `motivos_numero` (linha 130).

reservadas: Palavras

**t_ATRIB**, **t_MAIS**, **t_MENOS**, **t_DIV**: `=` `+` `-` `/`.

**t_PONTO** (linha 169): `.` termina o comando.

**t_VIRGULA** (linha 170): `,` separa parâmetros.

**t_ABRE_PAR** e **t_FECHA_PAR**: `(` `)`.

**t_ignore_COMENTARIO**: de `*` até o fim da linha é comentário e é ignorado.

**t_ignore**: espaço, tab, `\r` são ignorados.

**t_newline**: `\n` não gera token, só conta as linhas.

**t_error**: qualquer outro caractere é erro léxico e é pulado.
