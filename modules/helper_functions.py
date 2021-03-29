#!/usr/bin/env python
"""Helper functions for reshaping dictionaries for effieciency and timing."""

import csv
import os
import xml.etree.cElementTree as ET
from collections import OrderedDict

import pandas as pd
import numpy as np
import pprint

def dictionary_key_length_ordered_descending(mapping):
    """ Convert dictionary to ordered dictionary, ordered by key length descending.

    Dictionary for correction functions needs to be ordred to prevent general corrections
    from making corrections to street names requiring specific corrections.

    Example: 'N. IH35,' being corrected to 'N. I-35' instead of North I-35' due to 
    matching the correction for 'IH35,' (without the North correction).
    """
    
    street_mappings = [(k, v) for k, v in mapping.items()]
    street_mappings = sorted(street_mappings, key=lambda t: len(t[0]), reverse=True)
    return OrderedDict(street_mappings)


# ********************************* Phone Numbers helper *********************************


def phone_partial_clean(phones = {}):
    """ Takes dictionary of phone numbers to be fixed (as key).
    Removes parenthesis and inserts hyphen (-) in place of blanks
    saving partially cleaned number as value.

    Function is used prior to cleaning and reduces the number of 
    manual corrections needed in the update_phones mapping dictionary.
    """
    
    if not phones:
        phones = {'(512) 246-7941': 'fix_number',
        '+1 (512) 469-7000': 'fix_number',
        '+1 (512) 759-5900': 'fix_number',
        '+1 512 218 5062': 'fix_number',
        '+1 512 218 9888': 'fix_number',
        '+1 512 238 0820': 'fix_number',
        '+1 512 244 3737': 'fix_number',
        '+1 512 248 7000': 'fix_number',
        '+1 512 252 1133': 'fix_number',
        '+1 512 255 7000': 'fix_number',
        '+1 512 255 7530': 'fix_number',
        '+1 512 258 8114': 'fix_number',
        '+1 512 277 6959': 'fix_number',
        '+1 512 310 7600': 'fix_number',
        '+1 512 310 7678': 'fix_number',
        '+1 512 324 4000': 'fix_number',
        '+1 512 341 1000': 'fix_number',
        '+1 512 362 9525': 'fix_number',
        '+1 512 402 7811': 'fix_number',
        '+1 512 528 7000': 'fix_number',
        '+1 512 532 2200': 'fix_number',
        '+1 512 600 0145': 'fix_number',
        '+1 512 637 6890': 'fix_number',
        '+1 512 733 9660': 'fix_number',
        '+1 512 990 5413': 'fix_number',
        '+1 512)351 3179': 'fix_number',
        '+1 512-244-8500': 'fix_number',
        '+1 512-260-5443': 'fix_number',
        '+1 512-260-6363': 'fix_number',
        '+1 512-310-8952': 'fix_number',
        '+1 512-338-8805': 'fix_number',
        '+1 512-341-7387': 'fix_number',
        '+1 512-421-5911': 'fix_number',
        '+1 512-535-5160': 'fix_number',
        '+1 512-535-6317': 'fix_number',
        '+1 512-733-6767': 'fix_number',
        '+1 512-851-8777': 'fix_number',
        '+1 737 757 3100': 'fix_number',
        u'+1-737-484\u20110700': 'fix_number',
        '+1512-413-9671': 'fix_number',
        '+1512-909-2528': 'fix_number',
        '+15123885728': 'fix_number',
        '+15124282300': 'fix_number',
        '+15124648382': 'fix_number',
        '1+512-696-5209': 'fix_number'}
    
    for key in phones:
        phone_update_value = key.replace('(', '').replace(')', '').replace(' ', '-')
        phones[key] = phone_update_value

    pprint.pprint(phones)
    return phones

# ********************************* CSV write new header helper *********************************

def create_sample(OSM_FILE = "data\\round_rock.xml",
                  output_file = "data\\round_rock_sample.xml", 
                  reduce_by_factor = 23
                  ):
    """ Create a smaller sample osm file for testing

          Keyword arguments:
          OSM_File -- string .osm or .xml file path (default "data\\round_rock.xml")
          output_file  -- string output file path (default "data\\round_rock_sample.xml")
          reduce_by_factor -- integer value to reduce number of rows in file and file size (default 23)
    """

    osm_file = OSM_FILE
    SAMPLE_FILE = output_file
    k = reduce_by_factor # Parameter: take every k-th top level element

    def get_element(osm_file, tags=('node', 'way', 'relation')):
        """Yield element if it is the right type of tag

        Reference:
        http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
        """
        context = iter(ET.iterparse(osm_file, events=('start', 'end')))
        _, root = next(context)
        for event, elem in context:
            if event == 'end' and elem.tag in tags:
                yield elem
                root.clear()


    with open(SAMPLE_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write('</osm>')


# ********************************* get_file_info() helper *********************************

def get_file_info(dw_file_paths = ['data/round_rock.xml', 
                                   'sql/round_rockdb.db', 
                                   'sql/csv/nodes_tags.csv', 
                                   'sql/csv/nodes.csv', 
                                   'sql/csv/ways_nodes.csv', 
                                   'sql/csv/ways_tags.csv', 
                                   'sql/csv/ways.csv'
                                   ]):

    """ Get file name and size information (MB) from list of files paths.
    
        Keyword arguments:
            dw_file_paths -- list of string file paths (default 
                                  ['data/round_rock.xml', 
                                   'sql/round_rockdb.db', 
                                   'sql/csv/nodes_tags.csv', 
                                   'sql/csv/nodes.csv', 
                                   'sql/csv/ways_nodes.csv', 
                                   'sql/csv/ways_tags.csv', 
                                   'sql/csv/ways.csv'
                                   ]):
    
    """

    dw_file_paths = ['data/round_rock.xml', 'sql/round_rockdb.db', 'sql/csv/nodes_tags.csv', 'sql/csv/nodes.csv', 'sql/csv/ways_nodes.csv', 'sql/csv/ways_tags.csv', 'sql/csv/ways.csv']

    for path in dw_file_paths:
        file_name = path.split('/')[-1]
        file_size = str(int(os.path.getsize(path)/(1024*1024))) + ' MB'
        marker_count = 35 - len(file_name) - len(file_size)
        print(path.split('/')[-1] + ('.')*marker_count + str(file_size))



# ********************************* table_row_counts() helper *********************************

def table_row_counts(db_file = '', sql_statement_list = []):
    """ Get the table row counts and output in string: 
            'The [table_name] table has [number of rows].\n'

        Keyword arguments:
           db_file -- database file path
           sql_statement_list -- list of sql statments in the form:
                'Select count(*) as "[alias required]" FROM [table name];'

    """
    from modules.process_sql import sql_query

    if db_file == '' or len(sql_statement_list) == 0:
        print("\nERROR!: Missing parameters db_file path and/or list of sql statements\n\n"
              "table_row_counts( db_file = ' path to db '  ,  sql_statement_list = ['sql statment1', 'sql statement2', ...])\n\n"
              "\tsql_statement format:  'Select count(*) as \"[alias required]\" FROM [table name];' " )
        return

    for sql_statement in sql_statement_list:
        table_name = sql_statement.rstrip(';"\' ').split(' ')[-1]
        counts_obj = sql_query(db_file, sql_statement, False)
        for item in counts_obj:
            counts = counts_obj[item][0]
        
        print("The {} table has {} rows. \n".format(table_name, counts))



