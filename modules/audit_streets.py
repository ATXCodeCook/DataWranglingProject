#!/usr/bin/env python
"""Audit and update street names in nodes and ways."""

import xml.etree.cElementTree as ET
from collections import defaultdict, OrderedDict
import re

import pprint

# Handle imports for script calls versus function calls
try:
    from modules.helper_functions import dictionary_key_length_ordered_descending
except ImportError:
    from helper_functions import dictionary_key_length_ordered_descending

OSMFILE = "data\\round_rock.xml"
street_type_re = re.compile(r'[^a-zA-Z0-9 \']|\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)
# streets_not_in_dictionary =set()

expected_list = ['Avenue', 'Bend', 'Boulevard', 'Branch', 'Circle', 'Commons', 'Court', 'Cove', 
            'Crossing', 'Drive', 'Expressway', 'Flyway', 'Gap', 'Garden', 'Hill', 'Hollow', 
            'Horizon', 'Knoll', 'Landing', 'Lane', 'Loop', 'Park', 'Parkway', 'Pass', 'Path', 
            'Pathway', 'Place', 'Ravine', 'Riverwalk', 'Road', 'Run', 'Spring', 'Spur', 
            'Square', 'Street', 'Terrace', 'Trace', 'Trail', 'View', 'Walk', 'Way']

expected = set(expected_list)


# Mapping created from audit. Entire street names included along with 
# street types to reduce loop/dictionary calls when validating correction function.
mapping = {
            "Crossings" : "Crossing",
            "Dalmahoy" : "Dalmahoy Drive",
            "Edenderry" : "Edenderry Drive",
            "Canyon Maple" : "Canyon Maple Road",
            "St Marys" : "St Mary's Drive",
            "MCNEIL RD" : "McNeil Road",
            "Stonebridge" : "Stonebridge Drive",
            "Canterwood" : "Canterwood Lane",
            "Talamore" : "Talamore Road",
            "Trail Dust" : " Trail Dust Drive",
            "Brown Juniper" : "Brown Juniper Way",
            "Buckskin" : "Buckskin Drive",
            "Barrhead" : "Barrhead Cove",
            "Royal Dublin" : "Royal Dublin Drive",
            "Royal Pointe" : "Royal Pointe Drive",
            "Casitas" : "Casitas Drive",
            "Caisteal Castle" : "Caisteal Castle Path",
            "Raglan CastlePath" : "Raglan Castle Path",
            "Canyon Maple" : "Canyon Maple Drive",
            "Mellow Meadows" : "Mellow Meadows Drive",
            "Monarch Butterfly" : "Monarch Butterfly Way",
            "Murchison Ridge" : "Murchison Ridge Trail",
            "University Blvd" : "University Boulevard",
            "Louis Henna Blvd, TX 45 Frontage Road" : "Louis Henna Boulevard",
            "South IH35" : "South I-35",
            "Highway Interstate 35" :"I-35",
            "South Interstate 35, #260" : "South I-35",
            "South Interstate 35" : "South I-35",
            "South Interstate Highway 35" : "South I-35",
            "South Interstate 35" : "South I-35",
            "North I-35 Suite 298" : "North I-35",
            "North Interstate 35" : "North I-35",
            "North Interstate Hwy 35" : "North I-35",
            "North Interstate Hwy 35, Round Rock, TX 78681" : "North I-35",
            "Interstate Highway 35 Frontage Road" : "I-35",
            "State Highway 45 Frontage Road" : "SH 45",
            "Interstate Highway 35 Service Road" : "I-35",
            "North Interstate Highway 35 Frontage Road" : "North I-35",
            "North Interstate Highway 35 Service Road" : "North I-35",
            "North IH 35 Pflugerville" : "North I-35",
            "North I -35" : "North I-35",
            "North IH 35" : "North I-35",
            "North IH35" : "North I-35",
            'North IH35,': 'North I-35',
            "North IH 35" : "North I-35",
            "North IH-35" : "North I-35",
            "IH 35 North" : "North I-35",
            "TX 130 Frontage Road" : "North State Highway 130",
            "North SH 130 NB" : "North State Highway 130",
            "North Sh 130" : "North State Highway 130",
            "North FM 620" : "North Farm to Market 620",
            "FM 620 North" : "North Farm to Market 620",
            "Ranch Rd 620 N" : "North Ranch Road 620",
            "RR 620" : "Ranch Road 620",
            "FM 1325" : "Farm to Market 1325",
            "FM 1460" : "Farm to Market 1460",
            "FM 685" : "Farm to Market 685",
            "North RM 620" : "North Ranch Road 620",
            "North FM 620 Bldg 2" : "North Farm to Market 620",
            "Ranch-to-Market Road 620" : "Ranch Road 620",
            "East Whitestone Blvd T100, Cedar Park, TX 78613, United States" : "East Whitestone Boulevard",
            "Pecan Park Ste 300, Cedar Park, TX" : "Pecan Park Boulevard",
            "South Bell Blvd, Suite 301" : "South Bell Boulevard",
            "East Whitestone Blvd Ste G-145" : "East Whitestone Boulevard",
            "US Highway 183" : "US 183",
            "North Hwy 183" : "North US 183",
            "North Highway 183" : "North US 183",
            "Highway 183 North" : "North US 183",
            "Toll" : "Toll Road",
            "183A Frontage Road" : "183A Toll Road",
            "St": "Street",
            "Rd" : "Road",
            "Ave" : "Avenue",
            "Trl" : "Trail",
            "Blvd" : "Boulevard",
            "Cv" : "Cove",
            "Dr" : "Drive",
            "pass" : "Pass",
            "US-79" : "US 79",
            "IH-35" : "I-35",
            "IH35," : "I-35",
            "IH35" : "I-35",
            "RM 620" : "Ranch Road 620",
            "North" : '',
            "East" : '',
            "South" : '',
            "West" : '',
            "NB" : '',
            }

direction_mapping = { "N " : "North ", "S " : "South ", "E " : "East ", "W " : "West " }

# Mapping created from audit. Entire street names included along with 
# street types to reduce loop/dictionary calls when validating correction function.
street_mapping = dictionary_key_length_ordered_descending(mapping)


# ***************************  audit_street_validate_corrections()  ***************************

def audit_street_validate_corrections(OSM_FILE = "data\\round_rock.xml"):
    """ Takes .osm or .xml file and audits streetnames for uniformity.

    Compares addr:street values to expected endings and adds name to street_types
    dictionary if ending is not in expected list. The street_types list is then 
    printed to be manually reviewed for correciton decisions. Test corrections 
    are preprocessed to remove periods and left strip any leading digits or spaces. 
    Then they are added to mappings as needed to be used to validate the corrections. 
    Total changes are printed along with a no_change_list of street names programatically 
    identified for change but not changed. 
    
    The no_change_list is used for validation processing and should display wellformed 
    street names ending with numbers. It may also be an empty list if all street names 
    are in expected list or changed using the mappings.

    The streets_not_in_dictionary are streets that met the cleaning criteria but where not
    in the dictionary (returned a value of None). 
    
    The mappings are processes to create a street_mapping OrderedDict, ordered by length of 
    key ascending. This must be done to prevent general corrections for more specific corrections
    needed (see Example in module's docstring above).
    """

    def audit_street_type(street_types, street_name):
        """Check streetnames not in expected for pattern and add to street_type dictionary."""
        m = street_type_re.search(street_name)                                  
        if m:                                                                   
            street_type = m.group()                                             
            if street_type not in expected:                                     
                street_types[street_type].add(street_name)      
                               

    def is_street_name(elem):
        return (elem.attrib['k'] == "addr:street")   


    def audit(osmfile):
        """Get child tags of nodes and ways and start audit process"""                                                         
        # osm_file = open(osmfile, "r")
        with open(osmfile, "r", encoding="UTF-8") as osm_file:

            for event, elem in ET.iterparse(osm_file, events=("start",)):

                if elem.tag == "node" or elem.tag == "way":
                    for tag in elem.iter("tag"):
                        if is_street_name(tag):                                     
                            audit_street_type(street_types, tag.attrib['v'])        
            osm_file.close()
            return street_types


    def preprocess_streetname(street_name):
        """Pre-process streetname by:

            Removing abbrieavation periods.
            Replacing direction abbreviations followed by a space with direction full name.
            Strip beginning house number from streetname then process streetnames using street_mapping dictionary
        """
        street_name = street_name.replace('.', '')

        if street_name[0].isdigit() and street_name[0:4] != '183A':
            street_name = street_name.lstrip('01234567890 ')
        
        if street_name[0:2] in direction_mapping.keys():
            street_chars = street_name[0:2]
            street_name = street_name.replace(street_chars, direction_mapping[street_chars])

        return street_name


    def update_name(name, street_mapping):
        """Update the streetname. """

        name = preprocess_streetname(name)

        for key in street_mapping.keys():
            if name.endswith(key):
                name = name.replace(key, street_mapping[key])
        return name

    def audit_update_street():
        """Flow control function for auditing and validating update."""
        counter = 0
        no_change_list = []
        st_types = audit(OSM_FILE)                                                 
        pprint.pprint(dict(st_types))                                             
        print()

        for st_type, ways in st_types.items():                               
            for name in ways:
                                                            
                better_name = update_name(name, street_mapping)                          
                print(name, "=>", better_name)
                if name == better_name:
                    no_change_list.append((name, better_name))
                counter += 1

        print("\nTotal Changes: " + str(counter))
        print("\nThe following street names were identified but " \
            "no changes were made \n")
        pprint.pprint(no_change_list)

    audit_update_street()

if __name__ == "__main__":
    audit_street_validate_corrections(OSM_FILE = "data\\round_rock_sample.xml")