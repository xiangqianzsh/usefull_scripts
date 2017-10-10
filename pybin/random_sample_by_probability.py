import random
import argparse

def sample(f_in, p=0.01):
    '''f_in: input
        p: the probability every line be choosen
    '''
    for line in f_in:
        random_value = random.uniform(0, 1)
        if random_value < p:
            print line.rstrip()

def main(argv):
    cmdparser = argparse.ArgumentParser(description=''' random sample,
                                                    input: stdin, output: stdout,
                                                    example: cat test.txt | python random_sample_by_probability.py -p 0.01 > out.txt
                                                    ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    cmdparser.add_argument('-p', '--probability', default=0.01, type=float, help='the probability every line be choosen')
    args = cmdparser.parse_args(argv)
    sample(f_in=sys.stdin,
            p=args.probability,
            )

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

