#!/usr/bin/env python
"""Audit phones (phone numbers)"""

import xml.etree.cElementTree as ET
import re

import pprint

phone_re = re.compile(r'^\+1-[2-9]\d{2}-\d{3}-\d{4}$')

# dictionary for lookup searches
malformed_numbers = {}
wellformed_numbers = set()
duplicate_numbers = set()
did_not_catch = []

# **************************************  audit_phone() ************************************

def audit_phone(phone_number):
    """Checks if phone number follows the pattern +1-###-###-#### (US phone pattern)

    Separates phone numbers into Wellformed and Malformed numbers based on standard
    US pattern including country code. Identifies duplicate numbers found.

    Prints summary of information and the malformed dictionary of numbers and returns 
    malformed dictionary which can then be run through the phone_partial_clean function
    in helper_functions for partial cleaning.
    """
    wellformed = phone_re.search(phone_number)

    if phone_number in malformed_numbers.keys() or phone_number in wellformed_numbers:
        duplicate_numbers.add(phone_number)

    elif wellformed:                                                                   
        explore_phone_number = wellformed.group()                                             
        wellformed_numbers.add(explore_phone_number)
    
    elif phone_number:
        malformed_numbers[phone_number] = 'fix_number'
    else:
        did_not_catch.append(phone_number)



# **************************************  print_audit_phone_results() ************************************

def print_audit_phone_results(print_list):
    """ Print results of phone audit. """

    if isinstance(print_list, str) and print_list.lower() == 'all':
        print_type_list = ['malformed', 'duplicate', 'wellformed'] 
    elif isinstance(print_list, list):
        print_type_list = print_list.copy()
    elif isinstance(print_list, str):
        print_type_list.append(print_list)        


    if did_not_catch:
        print('\n*** Did not check these numbers. ***\n')
        pprint.pprint(did_not_catch)
    else:
        print("\nAll phone numbers were checked.\n")
    
    print("There are {} malformed numbers, {} duplicate numbers and {} wellformed numbers.\n"
            .format(len(malformed_numbers), len(duplicate_numbers), len(wellformed_numbers)))

    for item in print_type_list:

        if 'malformed' == item:
            print("The malformed numbers found are: \n")
            pprint.pprint(malformed_numbers)
        elif 'duplicate' == item:
            print('\nThe {} duplicated items are: \n'.format(len(duplicate_numbers)))
            print(duplicate_numbers)
        elif 'wellformed' == item:
            print('\nWellformed has {} items: \n'.format(len(wellformed_numbers)))
            pprint.pprint(wellformed_numbers)
        else:
            print('Pass "malformed", "wellformed", "duplicate" or "All" as paramaters to print dictionary of numbers.')



# **************************************  audit_phones() ************************************

def audit_phones(OSM_FILE = "data\\round_rock.xml", 
                 print_number_type = ['malformed', 'duplicate']):
    """ Audit phone and confirm they follow US phone structure of +1-###-###-####."""
                                                            
    # clear persistent data
    malformed_numbers.clear()
    wellformed_numbers.clear()
    duplicate_numbers.clear()
    did_not_catch.clear()

    # osm_file = open(OSM_FILE, "r")
    with open(OSM_FILE, "r", encoding="UTF-8") as osm_file:
        for event, elem in ET.iterparse(osm_file, events=("start",)):

            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == 'phone':                                     
                        audit_phone(tag.attrib['v'])        
        osm_file.close()

        print_audit_phone_results(print_number_type)

        print('\n Note: The returned malformed number dictionary can be run through \n' \
               '\tmodules.helper_functions phone_partial_clean(phone_dict) \n' \
               '\tfunction to partially clean the numbers given in the key.\n')

        return malformed_numbers

if __name__ == "__main__":
    audit_phones(OSM_FILE = "data\\round_rock_sample.xml")
    