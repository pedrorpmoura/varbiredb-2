import functools

import ply.yacc as yacc

from src.databases.formula_variational.queries.fvpure import FVPureQAnd, FVPureQOr, FVPureQSome, FVPureQNo, FVPureQIn, \
    FVPureQNot
from src.databases.sets_variational.queries.svpure import SVPureQSome, SVPureQNo, SVPureQIn, SVPureQNot, SVPureQOr, \
    SVPureQAnd
from src.query_parser.lexer import tokens
from src.databases.formula_variational.fvrelations import fvconverse, fvcomposition, fvdifference, fvintersection, \
    fvunion
from src.databases.non_variational.queries import NVQNot, NVQSome, NVQIn, NVQNo, NVQAnd, NVQOr
from src.databases.non_variational.relations import converse, composition, difference, intersection, union
from src.databases.sets_variational.svrelations import svconverse, svcomposition, svdifference, svintersection, svunion


class QueryParser:
    tokens = tokens

    def p_query_formula(self, p):
        """query : compose1"""
        p[0] = p[1]

    def p_compose1_or(self, p):
        """compose1 : compose1 OR compose2"""
        if self.mode == 'non_variational':
            p[0] = NVQOr(p[1], p[3])
        elif self.mode == 'fv_pure':
            p[0] = FVPureQOr(p[1], p[3])
        elif self.mode == 'sv_pure':
            p[0] = SVPureQOr(p[1], p[3])

    def p_compose1_one(self, p):
        """compose1 : compose2"""
        p[0] = p[1]

    def p_compose2_and(self, p):
        """compose2 : compose2 AND atomic"""
        if self.mode == 'non_variational':
            p[0] = NVQAnd(p[1], p[3])
        elif self.mode == 'fv_pure':
            p[0] = FVPureQAnd(p[1], p[3])
        elif self.mode == 'sv_pure':
            p[0] = SVPureQAnd(self.database['configurations'], p[1], p[3])

    def p_compose2_one(self, p):
        """compose2 : atomic"""
        p[0] = p[1]

    def p_atomic_some(self, p):
        """atomic : SOME expression"""
        if self.mode == 'non_variational':
            p[0] = NVQSome(p[2])
        elif self.mode == 'fv_pure':
            p[0] = FVPureQSome(p[2])
        elif self.mode == 'sv_pure':
            p[0] = SVPureQSome(p[2])

    def p_atomic_no(self, p):
        """atomic : NO expression"""
        if self.mode == 'non_variational':
            p[0] = NVQNo(p[2])
        elif self.mode == 'fv_pure':
            p[0] = FVPureQNo(p[2])
        elif self.mode == 'sv_pure':
            p[0] = SVPureQNo(self.database['configurations'], p[2])

    def p_atomic_in(self, p):
        """atomic : expression IN expression"""
        if self.mode == 'non_variational':
            p[0] = NVQIn(p[1], p[3])
        elif self.mode == 'fv_pure':
            p[0] = FVPureQIn(p[1], p[3])
        elif self.mode == 'sv_pure':
            p[0] = SVPureQIn(self.database['configurations'], p[1], p[3])

    def p_atomic_not(self, p):
        """atomic : NOT atomic"""
        if self.mode == 'non_variational':
            p[0] = NVQNot(p[2])
        elif self.mode == 'fv_pure':
            p[0] = FVPureQNot(p[2])
        elif self.mode == 'sv_pure':
            p[0] = SVPureQNot(self.database['configurations'], p[2])

    def p_atomic_compose(self, p):
        """atomic : '(' compose1 ')'"""
        p[0] = p[2]

    def p_expression_plus(self, p):
        """expression : expression '+' term"""
        if self.mode == 'non_variational':
            p[0] = union(p[1], p[3])
        elif self.mode == 'fv_pure' or self.mode == 'fv_trivial':
            p[0] = fvunion(p[1], p[3])
        elif self.mode == 'sv_pure' or self.mode == 'sv_trivial':
            p[0] = svunion(p[1], p[3])

    def p_expression_and(self, p):
        """expression : expression '&' term"""
        if self.mode == 'non_variational':
            p[0] = intersection(p[1], p[3])
        elif self.mode == 'fv_pure' or self.mode == 'fv_trivial':
            p[0] = fvintersection(p[1], p[3])
        elif self.mode == 'sv_pure' or self.mode == 'sv_trivial':
            p[0] = svintersection(p[1], p[3])

    def p_expression_minus(self, p):
        """expression : expression '-' term"""
        if self.mode == 'non_variational':
            p[0] = difference(p[1], p[3])
        elif self.mode == 'fv_pure' or self.mode == 'fv_trivial':
            p[0] = fvdifference(p[1], p[3])
        elif self.mode == 'sv_pure' or self.mode == 'sv_trivial':
            p[0] = svdifference(self.database['configurations'], p[1], p[3])

    def p_expression_term(self, p):
        """expression : term"""
        p[0] = p[1]

    def p_term_dot(self, p):
        """term : term '.' term1"""
        if self.mode == 'non_variational':
            p[0] = composition(p[1], p[3])
        elif self.mode == 'fv_pure' or self.mode == 'fv_trivial':
            p[0] = fvcomposition(p[1], p[3])
        elif self.mode == 'sv_pure' or self.mode == 'sv_trivial':
            p[0] = svcomposition(p[1], p[3])

    def p_term_one(self, p):
        """term : term1"""
        p[0] = p[1]

    def p_term1_id(self, p):
        """term1 : ID"""
        p[0] = self.database['relations'][p[1]]

    def p_term1_converse(self, p):
        """term1 : '~' term1"""
        if self.mode == 'non_variational':
            p[0] = converse(p[2])
        elif self.mode == 'fv_pure' or self.mode == 'fv_trivial':
            p[0] = fvconverse(p[2])
        elif self.mode == 'sv_pure' or self.mode == 'sv_trivial':
            p[0] = svconverse(p[2])

    def p_term1_expression(self, p):
        """term1 : '(' expression ')'"""
        p[0] = p[2]

    def p_error(self, p):
        print('Query Parser: Syntax error!')

    def __init__(self, database, mode=None, configurations=None):
        self.parser = yacc.yacc(module=self)
        self.database = database
        self.mode = mode
        self.configurations = configurations
