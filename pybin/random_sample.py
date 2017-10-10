import random
import argparse

def sample(f_in, num=10, is_output_shuffle=False):
    '''f_in: input
        num: random choice number
    '''
    listt = f_in.readlines()
    listt = [line.rstrip() for line in listt if line.rstrip() != '']
    listt_num = len(listt)
    if num > listt_num:
        num = listt_num
    sample_idx_list = random.sample(range(listt_num), num)
    if not is_output_shuffle:
        sample_idx_list = sorted(sample_idx_list)
    for idx in sample_idx_list:
        print listt[idx]

def main(argv):
    cmdparser = argparse.ArgumentParser(description=''' random sample,
                                                    input: stdin, output: stdout,
                                                    example: cat test.txt | python random_sample.py -n 20 > out.txt
                                                    ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    cmdparser.add_argument('-n', '--num', default=10, type=int, help='number of random choice')
    cmdparser.add_argument('--is_output_shuffle', dest='is_output_shuffle', default=False, action='store_true', help='output ordered or shuffled')
    args = cmdparser.parse_args(argv)
    sample(f_in=sys.stdin,
            num=args.num,
           is_output_shuffle=args.is_output_shuffle
            )

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

