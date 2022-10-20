import ply.lex as lex

# Reserved words:
reserved = {
    'EVALUATE': 'EVALUATE'
}


# List of token names
# Moet nog uitgebreid worden: 
# Vergelijkingen
# Unary / binary? (minus)
# boolean vergelijkingen
tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

 # A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


data = '''
3 + 4 * 10
+ -20 * 2
'''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
    
# Vier soorten DAX expressies:

# 1. Calculations
# 1a. Measures
#     Naam + "=" + Formula
# 1b. Calculated columns
#     Naam + "=" + Formula
#     Tabel en kolom waaraan gekoppeld 
# 1c. Calculated tables
#     Naam + "=" + Formula
#     Tabel waaraan gekoppeld
# 1d. Row-level security formula's
#     Naam (van regel) 
#     "=" + Formula

# 2. Queries
#    EVALUATE (required keyword)
#    optional keywords:
#    - ORDER BY
#    - START AT
#    - DEFINE
#    - MEASURE
#    - VAR
#    - TABLE
#    - COLUMN

# 3. Formulas
#    Bestaan uit operators
#    Functies
#    Kolomreferenties
#    Tabelreferenties

# 4. Functions
#    Naam
#    Parameters

# 5. Variables
#    VAR ... RETURN
#    (technicallhy not a function, a keyword to store the result of an expression)
#    Introduceert meer een "mode" dan een echte formule

# Datatypes
DAX_DATATYPES = {
    "Whole Number"
    , "Decimal number"
    , "Boolean"
    , "Text"
    , "Date"
    , "Currency"
    , "N/A"
    , "Table"
}

# Context
# In de basis is context een soort stack waarin de data opnieuw geanalyseerd wordt

# Operators
# 1. Arithmetic unary operators
UNARY_OPERATORS = {
    "+"
    , "-"
}

BINARY_OPERATORS = {
    "+"
    , "-"
    , "*"
    , "/"
    , "^"
    , "="
    , "=="
    , ">"
    , "<"
    , ">="
    , "<="
    , "<>"
    , "&"
    , "&&"
    , "||"
    , "IN"
}

# Fully qualified name
# 'Tabelnaam'[kolomnaam]