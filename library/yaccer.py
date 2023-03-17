import ply.yacc as yacc
from library.lexer import tokens

# Precedence rules for the arithmetic operators
# precedence = (
#     ('left', 'AND'),
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'TIMES', 'DIVIDE'),
# )

def p_expression_evaluate(p):
    'expression : EVALUATE table_expression'
    p[0] = ('EVALUATE', p[2])

def p_table_expression(p):
    'table_expression : ROW LPAREN QUOTE IDENTIFIER QUOTE COMMA scalar_expression RPAREN'
    p[0] = ('ROW', p[4], p[7])

def p_scalar_expression(p):
    'scalar_expression : CALCULATE LPAREN aggregate_expression RPAREN'
    p[0] = ('CALCULATE', p[3])

def p_aggregate_expression(p):
    'aggregate_expression : SUM LPAREN column_reference RPAREN FILTER LPAREN table_name COMMA condition RPAREN'
    p[0] = ('SUM', p[3], 'FILTER', p[7], p[9])

def p_table_name(p):
    'table_name : IDENTIFIER'
    p[0] = p[1]

def p_column_reference(p):
    'column_reference : IDENTIFIER LBRACKET IDENTIFIER RBRACKET'
    p[0] = (p[1], p[3])

def p_rel_op(p):
    '''rel_op : EQUALS
              | GREATER
              | LESS
              | GREATEREQUAL
              | LESSEQUAL
              | NOTEQUAL'''
    p[0] = p[1]

def p_condition(p):
    '''condition : column_reference rel_op value
                 | condition AND condition'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], 'AND', p[3])

def p_value(p):
    '''value : NUMBER
             | QUOTE IDENTIFIER QUOTE'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error at '{p.value}'")


# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Build the parser
parser = yacc.yacc()
