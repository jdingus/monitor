import shutil
import datetime
import time
import os
import logging
import sys
import subprocess
from data_store import enter_data
"""
1.) Look for a raw_data_NAME.csv file.
2.) If file is present or has been changed, rename and move the file into /processing/NAME_TIMESTAMP .
3.) Run the state machine parser to determine START-STOP matches.
4.) Write Good Data to the sqlite3 database, move file into /wrotedb .
5.) Write all errors to a log file in /errors .

"""
def move(src, dest):
    try:
        shutil.move(src, dest)
    except IOError:
        logging.error("Unable to move file IOError")
        print 'Filename tried to move: ',src
        print 'Tried to move to: ',dest
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.INFO) #INFO

    cwd = os.path.abspath(os.path.curdir)
    machine = 'cnc570'
    raw_data_fname = '%s_raw_data.csv' %  machine
    # print raw_data_fname
    current_timestamp = time.strftime("%Y-%m-%d_%H%M%S")
    dest = '\\processing\\' + current_timestamp + '-' + raw_data_fname
    new_file_path = cwd+dest

    move(raw_data_fname,new_file_path)
    logging.debug("Moved: "+raw_data_fname+" To: "+new_file_path)
    # print new_file_path #print filename when it's moved

    enter_data(new_file_path)

    # run_command = 'python data_store.py'
    # args = ' -f ' + dest
    # to_run = run_command + args
    # print "Running Command: ",to_run
    # subprocess.call(to_run)





if __name__ == '__main__':
    main()