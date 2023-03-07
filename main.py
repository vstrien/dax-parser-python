from library.yaccer import parser

# Test the lexerr
data = '''EVALUATE 
    ROW("salesamount",
    CALCULATE (
        SUM ( Sales[Unit Price] ),
        FILTER (
            Product,
            Product[Color] = "Red" && Product[Weight] > 3
        )
    )
    )'''

parser.parse(data)