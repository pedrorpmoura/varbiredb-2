import ply.lex as lex

tokens = ['ID', 'SOME', 'NO', 'IN', 'AND', 'OR', 'NOT']

reserved = {
    'some': 'SOME',
    'no': 'NO',
    'in': 'IN',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

literals = ['+', '&', '-', '.', '~', '(', ')']


def t_ID(t):
    r'\w+'
    t.type = reserved.get(t.value, 'ID')
    return t


t_ignore = ' \n\t'


def t_error(t):
    print('Illegal character: ' + t.value[0])


lexer = lex.lex()
