#!/usr/bin/env python
"""Audit postcodes."""

import xml.etree.cElementTree as ET

import pprint

round_rock_postcodes = set(['78626', '78634', '78681', '78717', '78660', '78728', '78664', '78665', '78628'])
not_post_code = set()
checked_postcode = set()



# **************************************  audit_postcodes() ************************************

def audit_postcodes(postcode):
    """ Separates postcodes into known City post codes and those not listed as city postcodes."""

    if (postcode not in round_rock_postcodes) and (postcode not in not_post_code):
        not_post_code.add(postcode)

    elif postcode not in checked_postcode:
        checked_postcode.add(postcode)



# **************************************  print_audit_postcode_results() ************************************

def print_audit_postcode_results():
    """ Print results of audit_postcode. """

    missing_postcodes = round_rock_postcodes.difference(checked_postcode)
    if not missing_postcodes:
        print("\nThere was at least one instance of each Round Rock postcode "\
               "found in the data.\n")
    else:
        print("\nThe following are Round Rock postcodes not found in the data.\n")
        print(missing_postcodes)
    if not_post_code:
        print("\nThe following postcodes are not identified as Round Rock postcodes and need review.\n")
        print(not_post_code)
        print('\n')


# **************************************  explore_postcode_details() ************************************

def explore_postcode_details(OSM_FILE, postcode_list):
    """ Explore element information for specific postcodes (Helper)."""
    
    print("Started")
    # osm_file = open(OSM_FILE, "r")
    with open(OSM_FILE, "r", encoding="UTF-8") as osm_file:
        for event, elem in ET.iterparse(osm_file, events=("start",)):

            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == 'addr:postcode' and tag.attrib['v'] in postcode_list:
                        print("\nInformation for postcode {}:".format(tag.attrib['v']))                                    
                        
                        for tag in elem.iter("tag"):
                            print(tag.attrib['k'], tag.attrib['v'])        
        osm_file.close()

        print("\n\nEnd of postcode details.\n")



# ************************* update_postcode() *************************
postcode_mapping = {'78621' : '78681', '787664' : '78664', '78728-1275' : '78728'}

def update_postcode(postcode_value):
    """Update postcodes using mapping dictionary.
    
       Takes postcode value, updates using postcode_mapping
       dictionary and returns updated value.
    """
    postcode_mapping = {'78621' : '78681', '787664' : '78664', '78728-1275' : '78728'}

    if postcode_value not in postcode_mapping.keys():
        return postcode_value
    else:
        print(postcode_value, "cleaned to -->", postcode_mapping[postcode_value])
        return(postcode_mapping[postcode_value])


# **************************************  audit_postalcode() ************************************

def audit_postalcode(OSM_FILE = "data\\round_rock.xml"):
    """ Audit postcodes and validate if in city."""
                                            
    # osm_file = open(OSM_FILE, "r")
    with open(OSM_FILE, "r", encoding="UTF-8") as osm_file:
        for event, elem in ET.iterparse(osm_file, events=("start",)):

            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == 'addr:postcode':                                     
                        audit_postcodes(tag.attrib['v'])        
        osm_file.close()

        print_audit_postcode_results()
        # Test postcode cleaning function
        for item in not_post_code:
            if item in postcode_mapping.keys():
                clean_postcode = update_postcode(item)
        print('\n')
        return not_post_code
   
if __name__ == "__main__":
    audit_postalcode(OSM_FILE = "data\\round_rock_sample.xml")
 
    