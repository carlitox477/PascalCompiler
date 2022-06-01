#!/usr/bin/env python3
import sys
from lexical_analizer import source_code_to_lexems, read_source_code
from context import get_pascal_program_file_name_path
# from exception import SyntaxError

lista_pares = []
preanalisis = ''
atributo = ''
errorSintactico = False
errorPreanalisis = False
columna = 1
fila = 1


def getSiguienteToken() -> None:
    """Asigna a preanalisis el siguiente token y al atributo tambien"""
    global lista_pares, preanalisis, atributo, columna, fila
    par = lista_pares[0]
    preanalisis = par[0]
    if len(par) == 3:
        atributo = par[1]
    else:
        atributo = ''
    fila = (par[2])[1]
    columna = (par[2])[0]
    lista_pares = lista_pares[1:]


def report(lista: list) -> None:
    # Reportar un error de sintaxis
    global errorSintactico
    esperados = ""
    if len(lista) > 1:
        i = 0
        while i < len(lista):
            esperados += lista[i]
            i += 1
            if i < len(lista):
                esperados += ", "
    else:
        esperados = lista[0]
    errorSintactico = True
    if errorPreanalisis:
        print(f"ERROR de sintaxis: {columna}:{fila}" +
              f" se obtuvo {preanalisis} y se esperaba {esperados}")
        # raise SyntaxError
    else:
        print("ERROR de sintaxis: se obtuvo" +
              f"{atributo} y se esperaba {esperados}")
        # raise SyntaxError


def match_token(t: str) -> None:
    """se verifica si el simbolo de preanalisis coincide con el terminal t"""
    global errorPreanalisis
    if preanalisis == t and len(lista_pares) > 0:
        getSiguienteToken()
    elif preanalisis != t:
        errorPreanalisis = True
        report([t])


def check_attribute(lista: list) -> None:
    """Se verifica si el atributo de preanalisis coincide con algún atributo de
    la lista Si no coincide entonces reporta un error"""
    if atributo not in lista:
        report(lista)

# Procedimientos para simbolos no terminales

# Tipos de datos


def tipo_de_dato() -> None:
    # print("Preanalisis: "+preanalisis+" y el atributo: "+atributo)
    if preanalisis == 'TK_datatype':
        check_attribute(['integer', 'boolean'])
        match_token('TK_datatype')
    else:
        report(['TK_datatype'])

# Progamas y bloques


def programa() -> None:
    match_token('TK_program')
    match_token('TK_identifier')
    match_token('TK_semicolon')
    bloque()
    if len(lista_pares) == 0:
        if not errorSintactico:
            print("Programa sin errores sintacticos.")
    else:
        print("ERROR de sintaxis: hay sentencias luego del final de programa.")


def bloque() -> None:
    """Simbolo no terminal <bloque>"""
    if preanalisis == 'TK_var':
        parte_declaracion_de_variables()
    if preanalisis == 'TK_function':
        parte_declaracion_de_subrutinas()

    comando_compuesto()

# Declaración de variables


def parte_declaracion_de_variables() -> None:
    """Simbolo no terminal <parte_declaration_de_variables"""
    match_token('TK_var')
    declaracion_de_variables()
    match_token('TK_semicolon')
    while preanalisis == 'TK_identifier':
        declaracion_de_variables()
        match_token('TK_semicolon')


def declaracion_de_variables() -> None:
    """Simbolo no terminal <declaracion_de_variables>"""
    lista_de_identificadores()
    match_token('TK_colon')
    tipo_de_dato()


def lista_de_identificadores() -> None:
    """Simbolo no terminal <lista_de_identificadores>"""
    while(preanalisis == 'TK_identifier'):
        match_token('TK_identifier')
        if preanalisis == 'TK_comma':
            match_token('TK_comma')

# Declaración de sub-rutinas


def parte_declaracion_de_subrutinas() -> None:
    """Simbolo no terminal <parte_declaracion_de_subrutinas>"""
    while(preanalisis == 'TK_function' or preanalisis == 'TK_procedure'):
        if preanalisis == 'TK_function':
            declaracion_de_funcion()
            match_token('TK_semicolon')
        elif preanalisis == 'TK_procedure':
            declaracion_de_procedimiento()
            match_token('TK_semicolon')


def declaracion_de_funcion() -> None:
    """Simbolo no terminal <declaracion_de_funcion"""
    match_token('TK_function')
    match_token('TK_identifier')
    if preanalisis == 'TK_parenthesis':
        check_attribute(['OPPAR'])
        match_token('TK_parenthesis')
        parametros_formales()
        check_attribute(['CLPAR'])
        match_token('TK_parenthesis')
    match_token('TK_colon')
    tipo_de_dato()
    match_token('TK_semicolon')
    bloque()


def declaracion_de_procedimiento() -> None:
    """Simbolo no terminal <declaracion_de_procedimiento>"""
    match_token('TK_procedure')
    match_token('TK_identifier')
    if preanalisis == 'TK_parenthesis':
        match_token('TK_parenthesis')
        parametros_formales()
        match_token('TK_parenthesis')
    match_token('TK_semicolon')
    bloque()


def parametros_formales() -> None:
    """Simbolo no terminal <parametros_formales>"""
    seccion_declaracion_de_variables()
    while preanalisis == 'TK_semicolon':
        match_token('TK_semicolon')
        seccion_declaracion_de_variables()


def seccion_declaracion_de_variables() -> None:
    """Simbolo no terminal <seccion_declaracion_de_variables>"""
    if preanalisis == 'TK_var':
        match_token('TK_var')
    declaracion_de_variables()

# Comandos


def comando_compuesto() -> None:
    """Simbolo no terminal <comando_compuesto>"""
    match_token('TK_begin')
    comando()
    match_token('TK_semicolon')
    while preanalisis in ['TK_begin', 'TK_if',
                          'TK_identifier', 'TK_while', 'TK_read', 'TK_write']:
        comando()
        match_token('TK_semicolon')
    match_token('TK_end')


def comando() -> None:
    """Simbolo no terminal <comando>"""
    if preanalisis == 'TK_begin':
        comando_compuesto()
    elif preanalisis == 'TK_if':
        comando_condicional()
    elif preanalisis == 'TK_identifier':
        match_token('TK_identifier')
        comando2()
    elif preanalisis == 'TK_while':
        comando_repetitivo()
    elif preanalisis == 'TK_read':
        comando_lectura()
    elif preanalisis == 'TK_write':
        comando_salida()
    else:
        report(['TK_begin', 'TK_if', 'TK_identifier',
                'TK_while', 'TK_read', 'TK_write'])


def comando2() -> None:
    """simbolo no terminal <comando'>"""
    if preanalisis == 'TK_comma' or preanalisis == 'TK_assignment':
        resto_asignacion()
    elif preanalisis == 'TK_parenthesis':
        resto_llamada_funcion()


def resto_asignacion():
    """Simbolo no terminal <resto_asignacion>"""
    while preanalisis == 'TK_comma':
        match_token('TK_comma')
        match_token('TK_identifier')
    match_token('TK_assignment')
    expresion()


def resto_llamada_funcion() -> None:
    """Simbolo no terminal <resto_llamada_funcion>"""
    check_attribute(['OPPAR'])
    match_token('TK_parenthesis')
    lista_de_expresiones()
    check_attribute(['CLPAR'])
    match_token('TK_parenthesis')


def comando_repetitivo() -> None:
    """Simbolo no terminal <comando_repetitivo>"""
    match_token('TK_while')
    expresion()
    match_token('TK_do')
    comando()


def comando_lectura() -> None:
    """simbolo no terminal <comando_lectura>"""
    match_token('TK_read')
    check_attribute(['OPPAR'])
    match_token('TK_parenthesis')
    # match_token('TK_identifier')
    expresion_simple()
    check_attribute(['CLPAR'])
    match_token('TK_parenthesis')


def comando_salida() -> None:
    """simbolo no terminal <comando_salida>"""
    match_token('TK_write')
    check_attribute(['OPPAR'])
    match_token('TK_parenthesis')
    # match_token('TK_identifier')
    expresion_simple()
    check_attribute(['CLPAR'])
    match_token('TK_parenthesis')


def comando_condicional() -> None:
    """Simbolo no terminal <comando_condicional>"""
    match_token('TK_if')
    expresion()
    match_token('TK_then')
    comando()
    if preanalisis == 'TK_else':
        match_token('TK_else')
        comando()

# Operaciones / Expresiones


def expresion() -> None:
    """Simbolo no terminal <expresion>"""
    if preanalisis != 'TK_boolean_literal':
        expresion_simple()
        while preanalisis == 'TK_relOp':
            check_attribute(['GT', 'LT', 'EQ', 'LEQ', 'GEQ', 'DIF'])
            match_token('TK_relOp')
            expresion_simple()
    else:
        match_token('TK_boolean_literal')


def expresion_simple() -> None:
    """Simbolo no terminal <expresion_simple>"""
    if preanalisis == 'TK_arithOp':
        check_attribute(['ADD', 'SUB'])
        match_token('TK_arithOp')
    termino()
    while preanalisis == 'TK_arithOp' or preanalisis == 'TK_or':
        if preanalisis == 'TK_arithOp':
            check_attribute(['ADD', 'SUB'])
            match_token('TK_arithOp')
        else:
            match_token('TK_or')
        termino()


def termino() -> None:
    """Simbolo no terminal <termino>"""
    factor()
    while ((preanalisis == 'TK_arithOp' and
            (atributo == 'MUL' or atributo == 'DIV')) or
           preanalisis == 'TK_and'):
        if preanalisis == 'TK_arithOp':
            check_attribute(['MUL', 'DIV'])
            match_token('TK_arithOp')
        else:
            match_token('TK_and')
        factor()


def factor() -> None:
    """Simbolo no terminal <factor>"""
    if preanalisis == 'TK_identifier':
        match_token('TK_identifier')
        if preanalisis == 'TK_parenthesis' and atributo == 'OPPAR':
            resto_llamada_funcion()
    elif preanalisis == 'TK_number':
        match_token('TK_number')
    elif preanalisis == 'TK_not_literal':
        match_token('TK_not_literal')
        factor()
    elif preanalisis == 'TK_parenthesis':
        check_attribute(['OPPAR'])
        match_token('TK_parenthesis')
        expresion()
        check_attribute(['CLPAR'])
        match_token('TK_parenthesis')
    else:
        report(['TK_identifier', 'TK_number',
                'TK_not_literal', 'TK_parenthesis'])


def lista_de_expresiones() -> None:
    """Simbolo no terminal <lista_de_expresiones>"""
    expresion_simple()
    while preanalisis == 'TK_comma':
        match_token('TK_comma')
        expresion_simple()


def main() -> None:
    global lista_pares
    PASCAL_PROGRAM_FILE_NAME = sys.argv[1]
    source_code = read_source_code(get_pascal_program_file_name_path(
        PASCAL_PROGRAM_FILE_NAME))
    lista_pares = source_code_to_lexems(source_code)
    getSiguienteToken()
    programa()


if __name__ == '__main__':
    main()
