from tests.Tester import Tester
import matplotlib.pyplot as plt

options_path = 'src/generator/options.json'

if __name__ == '__main__':

    nv = []
    fv = []
    sv = []
    fs = range(4, 5)

    query = 'some Topic - Node.subscribes'

    for i in fs:
        options = {
            's': i,
            'p': i,
            'elements': 1001
        }

        tester = Tester(options)
        t1, t2, t3 = tester.run(query)

        nv.append(t1)
        fv.append(t2)
        sv.append(t3)

    print(nv)
    print(fv)
    print(sv)
    """
    nv = []
    fv = []
    sv = []
    fs = list(range(0, 12))

    
    for i in fs:
        print('---------------------------')
        print(f'[*] Generating graph for {i} features')
        options = {
            "featuresUniverse": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"],
            "numberOfActivatedFeatures": i,

            "featurePresenceProbability": 0.3,
            "conjunctionProbability": 0.5,
            "disjunctionProbability": 0.3,

            "setsUniverse": ["Node", "Topic", "Param"],
            "numberOfSets": 2,
            "numberOfElements": 50,

            "relationsUniverse": ["subscribes", "publishes", "param"],
            "numberOfRelations": 1,
            "typesOfRelations": [["$0", "$1"]],
            "presenceProbabilityOfRelations": [0.3]
        }

        tester = Tester(options)
        t1, t2, t3 = tester.run('no Node.subscribes - Topic')

        nv.append(t1)
        fv.append(t2)
        sv.append(t3)
    
    
    """
    plt.plot(fs, nv, label="Non-variational")
#
    plt.plot(fs, fv, label="Variational - Formulas")
#
    plt.plot(fs, sv, label="Variational - Sets")
#
    plt.xlabel('Number of features')
    ## Set the y axis label of the current axis.
    plt.ylabel('Execution Time')
    ## Set a title of the current axes.
    plt.title(query)
    ## show a legend on the plot
    plt.legend()
    # Display a figure.
    #plt.show()
    plt.savefig('features.png')
