import ply.yacc as yacc
from library.lexer import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_statement(p):
    'statement : EVALUATE table_expression'
    p[0] = ('EVALUATE', p[2])


def p_table_expression(p):
    'table_expression : ROW LPAREN STRING COMMA scalar_expression RPAREN'
    p[0] = ('ROW', p[3], p[5])

def p_scalar_calculate_expression(p):
    'scalar_expression : CALCULATE LPAREN aggregate_expression RPAREN'
    p[0] = ('CALCULATE', p[3])

def p_scalar_calculate_filter_expression(p):
    'scalar_expression : CALCULATE LPAREN aggregate_expression COMMA filter_expression RPAREN'
    p[0] = ('CALCULATE', p[3], p[5])

def p_scalar_value_expression(p):
    'scalar_expression : value'
    p[0] = ('VALUE', p[1])

def p_filter_expression(p):
    '''filter_expression : FILTER LPAREN table_name COMMA condition RPAREN'''
    p[0] = ('FILTER', p[3], p[5])

def p_aggregate_expression(p):
    'aggregate_expression : SUM LPAREN column_reference RPAREN'
    p[0] = ('SUM', p[3])

def p_table_name(p):
    'table_name : TABLEID'
    p[0] = p[1]

def p_column_reference_full(p):
    'column_reference : table_name COLUMNID'
    p[0] = (p[1], p[2])

def p_column_reference_short(p):
    'column_reference : COLUMNID'
    p[0] = (p[1])

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
                 | combined_condition'''
    p[0] = p[1]

def p_combined_condition(p):
    '''combined_condition : condition AND condition'''
    p[0] = (p[1], 'AND', p[3])

def p_value(p):
    '''value : NUMBER
             | STRING'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error at '{p}'")

# Build the parser
parser = yacc.yacc()
