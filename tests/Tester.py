import timeit

from src.configurations import convert_to_set
from src.controlled_generator.linear import generate_linear
from src.databases.formula_variational.helpers import solve
from src.generator.generator import Generator
from src.query_parser.parser import QueryParser

options_path = 'src/generator/options.json'


class Tester:

    def __init__(self, options):
        print("[*] Generating databases...")
        #g = Generator(options)
        #self.nv, self.fv, self.sv = g.generate()

        s = options['s']
        p = options['p']
        elements = options['elements']

        self.nv, self.fv, self.sv = generate_linear(s, p, elements)

    def run(self, query: str):
        r1 = set()

        def run_nv():
            for db in self.nv:
                #print(db)
                qp = QueryParser(db, mode='non_variational')
                parsed_query = qp.parser.parse(query)
                if parsed_query():
                    r1.add(db['configuration'])

        r2 = None

        def run_fv():
            qp = QueryParser(self.fv, mode='fv_pure')
            parsed_query = qp.parser.parse(query)
            nonlocal r2
            r2 = parsed_query()

        r3 = None

        def run_solve_fv():
            nonlocal r3
            r3 = solve(set(self.fv['features']), r2)

        r4 = None

        def run_sv():
            qp = QueryParser(self.sv, mode='sv_pure')
            parsed_query = qp.parser.parse(query)
            nonlocal r4
            r4 = parsed_query()

        t1 = timeit.timeit(run_nv, number=1)
        print(t1)

        t2 = timeit.timeit(run_fv, number=1)
        print(t2)

        t3 = timeit.timeit(run_solve_fv, number=1)
        print(t3)

        t4 = timeit.timeit(run_sv, number=1)
        print(t4)

        print(r1 == r3 == r4)
        print(r1)
        print(r2)
        print(r3)
        print(r4)


        #print(len(r1))
        # else:
        #    print([x for x in r1 if x not in r4])

        return t1, t2, t4
