#! /usr/bin/python
from start_stop import create_start_stop
from sqlite_module import write_list_data,initialize_tables,query_list_data
from optparse import OptionParser
import logging
import sys

def enter_data(fname):
    """ Pass fname using -f and will parse file and compose start stop strings
    using pkl to persist in between entries, when data entry is found will 
    write to sqlite3 db """

    print fname
    logging.debug("Creating start_stop list from: " + fname)
    start_stop = create_start_stop(fname)
    logging.debug(start_stop)
    logging.debug("Append start_stop list and append to a list: " + fname)
    data_entries = listdicts_to_listentries(start_stop)
    # initialize_tables()
    logging.debug("Writing to database: " + fname)
    for item in data_entries:
            write_list_data(item)
    query_list_data()

def argparser_add():
    USAGE = '''%prog -f fname'''
    parser = OptionParser(usage=USAGE)
    parser.add_option('-f', '--fname', dest='fname', help="Filename to perform action on", type='string')
    parser.add_option('-v', '--verbose', dest='verbose', help="Verbose mode",
    default=False, action='store_true')

    (opts, args) = parser.parse_args()
    if not opts.fname:
        parser.print_usage()
        sys.exit(1)

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    return opts,args

def convert_dict_to_commas(dict_in,col_order):
    '''Takes a dictionary and list of col_order to output in  and creates a csv line 
     of the values in the col_order given'''
    list_values = []
    for item in col_order:
        list_values.append(dict_in[item])
    return list_values

def listdicts_to_listentries(list_dicts):
    col_order = ['start_time','stop_time','cnc_id','prog_num','part1_num','part1_suf','part1_qty','part2_num','part2_suf','part2_qty','ref_input','pc_time','tc_time','prog_ct','ref_output']
    list_entries = []
    for ind_dict in list_dicts:
        single_entry = convert_dict_to_commas(ind_dict,col_order)
        list_entries.append(single_entry)
    return list_entries

if __name__ == '__main__':
    (opts,args) = argparser_add()
    enter_data()