#coding:utf8
import sys
import argparse

def trans_dsv_data(f_in=sys.stdin, f_out=sys.stdout,
                header_in=True, sep_in='\t', header_names=None,
                header_out=True, sep_out='\t',
                update_dict=None,
                drop_fields=None,
                keep_fields=None,
                ):
    ''' Trans dsv data. update value, keep/drop columns'
        header_names: None, []
        header_out: True/False
        update_dict: None, {}
        drop_fields: None, []
        keep_fields: None, []
    '''
    if update_dict == None:
        update_dict = {}

    if header_in:
        header = f_in.readline().rstrip().split(sep_in)
    else:
        assert header_names != None, 'give header_name if data has not header'
        header = header_names

    # keep_header without uniq
    if keep_fields:
        _keep_header = keep_fields
    else:
        _keep_header = header + update_dict.keys()
    if drop_fields:
        _keep_header = [k for k in _keep_header if k not in drop_fields]

    #uniq
    keep_header = []
    for k in _keep_header:
        if k not in keep_header:
            keep_header.append(k)

    assert len(keep_header) > 0, 'output fields number should greater than 0'  #last keep header

    if header_out:
        print >> f_out, sep_out.join(keep_header)
    for line in f_in:
        line = line.rstrip()
        if not line:
            continue
        fields = line.split(sep_in)
        record = dict(zip(header, fields))
        record.update(update_dict)  #update key values
        keep_fileds = [record[col] for col in keep_header]
        print >> f_out, sep_out.join(keep_fileds)


def main(argv):
    cmdparser = argparse.ArgumentParser(description='''Trans dsv data. update value, keep/drop columns.
                                        example:
                                        cat 20170615 | python ~/zhangshaohua02/pybin/trans_dsv_data.py --header_in --header_names sid,first_tc_success_pv,tc_success_pv,daoliu_zhuanma_click --update_values date:20170615
                                        ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    cmdparser.add_argument('--header_in', action='store_false', help='input has has header?')
    cmdparser.add_argument('--header_names', help='give header_name if header_in = False')
    cmdparser.add_argument('--header_out', action='store_false', help='output has header?')
    cmdparser.add_argument('--sep_in', default='\t', help='delimiter of input (default: tab %(default)s)')
    cmdparser.add_argument('--sep_out', default='\t', help='delimiter of output (default: tab %(default)s)')
    cmdparser.add_argument('--drop_fields', help='column names to drop, sep by ,')
    cmdparser.add_argument('--keep_fields', help='column names to keep, sep by , add all cols by default')
    cmdparser.add_argument('--update_values', help='update value of data like k1:v1,k2:v2,k3:v3')

    args = cmdparser.parse_args(argv)

    if args.update_values:
        update_dict = dict([k_v_pair.split(':') for k_v_pair in args.update_values.split(',')])
    else:
        update_dict = {}

    trans_dsv_data(header_in=args.header_in,
                sep_in=args.sep_in,
                header_names=args.header_names.split(',') if args.header_names else None,
                header_out=args.header_out,
                sep_out=args.sep_out,
                update_dict=update_dict,
                drop_fields=args.drop_fields.split(',') if args.drop_fields else None,
                keep_fields=args.keep_fields.split(',') if args.keep_fields else None,
                )

if __name__ == '__main__':
    main(sys.argv[1:])
