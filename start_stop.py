#! /usr/bin/python
import sys
import csv
import pickle
import collections

def main():
    ''' Parse data in csv file and manipulate as needed and compile start-stop 
    sequence to be returned in list format. Store ending state during parsing to be 
    used if needed '''
    start_stop = collections.OrderedDict()
    start_stop = create_start_stop('data_example.csv')
    write_startstop_csv(start_stop) # Once thru file write all start-stop to file
    print len(start_stop)

def create_start_stop(csv_file):
    ''' Parse data in csv file and manipulate as needed and compile start-stop 
    sequence for sqlite3 dbase write. Store ending state during parsing to be 
    used if needed, return resulting list of entries in dict format '''
    csv_list = load_csv(csv_file)
    csv_list = add_suffix(csv_list)
    csv_list = format_data(csv_list)

    start_stop = []
    for line in csv_list:
        for key in line:
            if isinstance(line[key], basestring):
                line[key] = line[key].strip() #strip any whitespace in strings
        ss = statemachine(line) # Pass each entry into statemachine
        if ss:                  # If statemachine returns start-stop match append
            start_stop.append(ss)
    return start_stop

    
def load_csv(file_name):
    col_names = ['date_time','action','cnc_id','prog_num','part1_num','part1_suf',
    'part1_qty','part2_num','part2_suf','part2_qty','ref_input','pc_time',
    'tc_time','prog_ct','ref_output']
    
    csv_file = csv.DictReader(open(file_name, 'rb'), delimiter=',',
     quotechar='"', fieldnames=col_names)
    
    csv_list=[]
    for line in csv_file:
        csv_list.append(line)
    return csv_list

def write_startstop_csv(csv_list):
    f = open('start_stop.csv', 'wb')
    keys = ['start_time','stop_time','cnc_id','prog_num','part1_num','part1_suf','part1_qty',
            'part2_num','part2_suf','part2_qty','ref_input','pc_time','tc_time','prog_ct',
            'ref_output']
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writer.writerow(keys)
    dict_writer.writerows(csv_list)

def calc_letter(digit):
    l=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    if (digit > 0 and digit <= 26):
        letter = l[digit-1]
    else:
        letter = ''
    return letter

def add_suffix(csv_list):
    for line in csv_list:
        suf_1 = int(line['part1_suf'])
        suf_2 = int(line['part2_suf'])

        if not suf_1 == 0:
            prt_1 = str(line['part1_num'])
            suffix = calc_letter(suf_1)
            prt_1_new = prt_1 + suffix
            line['part1_num'] = prt_1_new

        if not suf_2 == 0:
            prt_2 = str(line['part2_num'])
            suffix = calc_letter(suf_2)
            prt_2_new = prt_2 + suffix
            line['part2_num'] = prt_2_new
    return csv_list

def format_data(csv_list):
    for line in csv_list:
        line['pc_time'] = float(line['pc_time'])/1000 # convert to seconds
        line['tc_time'] = float(line['tc_time'])/1000 # convert to seconds
        # line['TIME_STAMP'] = datetime.strptime(line['TIME_STAMP'], "%m/%d/%y %H:%M:%S")  # convert to python time
    return csv_list

def reload_state():
    """ Reloads persisted state dictionary """
    try:
        afile = open(r'state.pkl', 'rb')
        d = pickle.load(afile)
        afile.close()
        return d
    except:
        initialize_state()
        print 'exception on state reload_state()'
        s = {'state':0,'action':'unknown','p1_num':'unknown'}
        return s

def initialize_state():
    state = {'state':0,'action':'unknown','part1_num':'unknown'}
    print 'initialized state file!'
    store_state(state)

def store_state(state):
    """ Persists state dictionary to file """
    afile = open(r'state.pkl', 'wb')
    pickle.dump(state, afile)
    afile.close()

def statemachine(d):
    '''Process line entries of data and match into start-stop sequences'''
    s = reload_state() # Using pikl reload previously stored state

    if d['action'] == 'START':
        s['state'] = 1
        s['part1_num'] = d['part1_num']
        s['start_time'] = d['date_time']
        s['action'] = 'START'
        store_state(s)
        return

    if s['state'] == 0:
        print 30*'*','STATE 0 and no START',30*'*','\n',d,30*'*'
        return
            
    elif s['state'] == 1:
        if (d['action'] == 'STOP' and d['part1_num'] == s['part1_num']):
            s['state'] = 2
            s['action'] = 'STOP'
            d['stop_time'] = d['date_time']
            d['start_time'] = s['start_time']
            d.pop("date_time", None)
            d.pop("action", None)
            store_state(s)
            # e = d
            # d = {}
            return d #e
        else: 
            s['state'] = 0
            s['action'] = d['action']
            s['part1_num'] = d['part1_num']
            store_state(s)
            print 30*'*','STATE 1 and no STOP MATCH',30*'*','\n',d,30*'*'
            return
        
    elif s['state'] == 2:
            s['state'] = 0
            s['action'] = d['action']
            s['part1_num'] = d['part1_num']
            store_state(s)
            print 30*'*','STATE 2 and no START',30*'*','\n',d,'\n',30*'*'
            return
    else:
        initialize_state()
        store_state(s)
        print 30*'*','STATE NOT 0,1 or 2 --> initialize_state()',30*'*','\n',d,'\n',30*'*'
        return

if __name__ == "__main__":   
    main()