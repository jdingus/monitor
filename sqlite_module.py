#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys

def main():
    query_list_data ()
    # drop_data_table()
    # create_data_table()
    # write_list_data(1)

def initialize_tables():
    drop_data_table()
    create_data_table()

def write_list_data(list_data):
    ''' Take a list of data entry lists and write to a table '''
    con = lite.connect('test.db')

    with con:
        cur = con.cursor()    
        query = 'INSERT INTO [data] VALUES(%s)' % ','.join(['?'] * len(list_data))
        cur.execute(query, list_data)


def query_list_data():
    ''' Query entried in the db '''
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        query = 'SELECT start_time,stop_time,part1_num FROM [data]'
        results = cur.execute(query)
        results=[]
        for row in cur:
            results.append(row)
        # print results   
        print len(results),' : Entries found.'

def drop_data_table():
    con = lite.connect('test.db')

    with con:
        cur = con.cursor()    
        cur.execute("DROP TABLE IF EXISTS [data]")

def create_data_table():
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        cur.execute("\
        CREATE TABLE [data] (\
        [start_time] TIMESTAMP NOT NULL ON CONFLICT ROLLBACK, \
        [stop_time] TIMESTAMP NOT NULL ON CONFLICT ROLLBACK, \
        [cnc_id] text NOT NULL ON CONFLICT ROLLBACK, \
        [prog_num] text, \
        [part1_num] TEXT, \
        [part1_suf] integer, \
        [part1_qty] integer, \
        [part2_num] TEXT, \
        [part2_suf] integer, \
        [part2_qty] integer, \
        [ref_input] float, \
        [pc_time] float, \
        [tc_time] float, \
        [prog_ct] float, \
        [ref_output] float)")

if __name__ == '__main__':
    main()

