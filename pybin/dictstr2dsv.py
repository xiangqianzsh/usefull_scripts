#coding:utf-8
import sys
import os
import argparse

'''
dictstr2dsv.py
input: line of python dict string (print dict)
    if you want your output to be orderd, please contain a key __output_fields__
output: csv/excel format data, sep by tab by default


for example:
# test.txt
{'__output_fields__': ['name', 'score'], 'score': 90, 'name': '\xe5\xbc\xa0\xe4\xb8\x89'}
{'__output_fields__': ['name', 'score'], 'score': 95, 'name': '\xe6\x9d\x8e\xe5\x9b\x9b'}

# cmd
cat test.txt | python dictstr2dsv.py --add_fields class:三.一班

'''

def main(argv, f_in=sys.stdin):
    cmdparser = argparse.ArgumentParser('parse input data and output excel/csv format data')
    cmdparser.add_argument('--header', default='on',
                                help='on/off, print header? (default on)')
    cmdparser.add_argument('--sep', default='\t', help='delimiter to use, default tab')
    cmdparser.add_argument('--add_fields', help='add fields value into input data, update if the field is already in input_data like: date:20160907,key:new_key')
    cmdparser.add_argument('--output_fields', help='choose fields to output, '
                                            'default: __output_fields__ + add_fileds or dict.keys() + add_fields')
    cmdparser.add_argument('--debug', action='store_true', default=False,
                                help='debug? (default False)')
    args = cmdparser.parse_args(argv)
    header_str = args.header
    if header_str == 'on':
        header = True
    else:
        header = False

    debug = args.debug

    #add fields
    add_fields = args.add_fields
    add_fields_name = []
    if add_fields == None:
        add_fields_dict = {}
    else:
        nest_list = [ele.split(':') for ele in add_fields.split(',')]
        add_fields_name = [ele[0] for ele in nest_list]
        add_fields_dict = dict(nest_list)

    sep = args.sep

    flag_first_line = True
    for line in f_in:
        line_dict = eval(line)
        if debug:
            print '============ new line ==============='
            print 'input line: ', line.rstrip('\n')
            print 'parsed dict: ', str(line_dict)

        line_dict.update(add_fields_dict) #update fields
        if flag_first_line:   #first line, make header_fields print heder if needed
            output_fields = args.output_fields  # output fields
            if output_fields == None:
                output_fields_name = line_dict.get('__output_fields__', line_dict.keys())
                output_fields_name += add_fields_name
            else:
                output_fields_name = output_fields.split(',')
            if header:  #header
                print sep.join(output_fields_name)
            flag_first_line = False
        line_fields = [str(line_dict[field]) for field in output_fields_name]
        print sep.join(line_fields)


if __name__ == '__main__':
    main(sys.argv[1:])

