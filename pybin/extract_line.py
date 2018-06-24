import sys
import argparse

def extract(f_in, lineno_list, add_lineno):
    '''f_in: input
    '''
    listt = [line.rstrip() for line in f_in]
    line_dict = dict(zip(range(1, len(listt) + 1), listt)) # linenu from 1
    for i in lineno_list:
        if i in line_dict:
            if add_lineno:
                print "%s\t%s" %(i, line_dict[i])
            else:
                print "%s" %line_dict[i]
        else:
            print >>sys.stderr, "Error, input has not lineno %s" %i

def main(argv):
    cmdparser = argparse.ArgumentParser(description='''extract by line by linenu, example, 
                                                    Example1: cat xx | python extract_line.py -n 1,2,3   
                                                    Example2: cat xx | python extract_line.py -f file
                                                    ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    cmdparser.add_argument('-n', '--lineno', default="", help='line numbers, from 1, example 1,2,3,4,5')
    cmdparser.add_argument('-f', '--file', help='use line nu in a file')
    cmdparser.add_argument('-a', '--add_lineno', default=False, action='store_true', help='add lineno in output file')
    args = cmdparser.parse_args(argv)

    lineno_list = []
    if args.lineno != "":
        lineno_list = map(int, args.lineno.split(","))
    else: # use lineno in file
        with open(args.file) as f:
            lineno_list = [int(line.strip()) for line in f if line.strip() != ""]
    extract(sys.stdin, lineno_list, args.add_lineno)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

