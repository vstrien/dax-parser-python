import ply.lex as lex

# Reserved words:
statements = {
    'EVALUATE': 'EVALUATE',
    'DEFINE': 'DEFINE',
}

# functions
functions = {
    'FILTER': 'FILTER',
    'ROW': 'ROW',
    'SUM': 'SUM',
    'CALCULATE': 'CALCULATE',
}
# List of token names
# Moet nog uitgebreid worden:
# Vergelijkingen
# Unary / binary? (minus)
# boolean vergelijkingen
tokens = list(statements.values()) + list(functions.values()) + [
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLON',
    'SEMICOLON',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'POWER',
    'NUMBER',
    'STRING',
    'WHITESPACE',
    'AMPERSAND',
    'GREATER',
    'LESS',
    'GREATEREQUAL',
    'LESSEQUAL',
    'NOTEQUAL',
    'AND',
    'TABLEID',
    'COLUMNID',
]

# Define the regular expression for each token
t_EVALUATE = r'EVALUATE'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_POWER = r'\^'
t_WHITESPACE = r'\s+'
t_AND = r'\&\&'
t_AMPERSAND = r'\&'
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL =r'<='
t_NOTEQUAL =r'<>'
t_FILTER = r'FILTER'
t_CALCULATE = r'CALCULATE'
t_ROW = r'ROW'
t_SUM = r'SUM'

def t_TABLEID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = statements.get(t.value, functions.get(t.value, 'TABLEID')) # Check for reserved words
    return t

def t_COLUMNID(t):
    r'\[[a-zA-Z_ ]+\]'
    t.value = t.value[1:-1] # strip off the brackets
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1] # strip off the double quotes
    return t

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

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
    "Whole Number", "Decimal number", "Boolean", "Text", "Date", "Currency", "N/A", "Table"
}

# Context
# In de basis is context een soort stack waarin de data opnieuw geanalyseerd wordt

# Operators
# 1. Arithmetic unary operators
UNARY_OPERATORS = {
    "+", "-"
}

BINARY_OPERATORS = {
    "+", "-", "*", "/", "^", "=", "==", ">", "<", ">=", "<=", "<>", "&", "&&", "||", "IN"
}

# Fully qualified name
# 'Tabelnaam'[kolomnaam]
