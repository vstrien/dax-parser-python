import ply.yacc as yacc
from lexer import tokens

# Define the grammar rules
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_power(p):
    'factor : factor POWER primary'
    p[0] = p[1] ** p[3]

def p_factor_primary(p):
    'factor : primary'
    p[0] = p[1]

def p_primary_float(p):
    'primary : FLOAT'
    p[0] = float(p[1])

def p_primary_identifier(p):
    'primary : IDENTIFIER'
    p[0] = p[1]

def p_primary_function(p):
    'primary : FUNCTION args'
    p[0] = p[1]

def p_args(p):
    'args : LPAREN arglist RPAREN'
    p[0] = p[2]

def p_arglist_single(p):
    'arglist : expression'
    p[0] = [p[1]]

def p_arglist_multi(p):
    'arglist : arglist COMMA expression'
    p[0] = p[1] + [p[3]]

# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error: {p}")

# Build the parser
parser = yacc.yacc()
