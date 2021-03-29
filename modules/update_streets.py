#!/usr/bin/env python
"""Audits and Updates street names with tags addr:street.

expected_street_list holds known good values for street ending types
for the area (found through auditing the data).

street_mapping hold street ending types and street name problems found
during auditing.
"""
import re
from collections import defaultdict, OrderedDict

street_type_re = street_type_re = re.compile(r'[^a-zA-Z0-9 \']|\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)
row_countme = 0


expected_street_list = ['Alemeda', 'Avenue', 'Bend', 'Boulevard', 'Branch', 'Circle', 'Commons', 'Court', 'Cove', 
            'Crossing', 'Drive', 'Expressway', 'Flyway', 'Gap', 'Garden', 'Hill', 'Hollow', 
            'Horizon', 'Knoll', 'Landing', 'Lane', 'Loop', 'Park', 'Parkway', 'Pass', 'Path', 
            'Pathway', 'Place', 'Ravine', 'Riverwalk', 'Road', 'Run', 'Spring', 'Spur', 
            'Square', 'Street', 'Terrace', 'Trace', 'Trail', 'View', 'Walk', 'Way']

# end_in_number = set(["County Road 138", "North Ranch Road 620", "Ranch Road 620", "State Highway 130", "County Road 137", 
#                      "County Road 176", "County Road 172", "County Road 170", "Farm to Market 685", "Farm to Market 1325", "County Road 112", "US 183",
#                      "I-35", "US 79", "North State Highway 130", 'South I-35','North I-35', 'North US 183'])

direction_mapping = { "N " : "North ", "S " : "South ", "E " : "East ", "W " : "West " }

# Add string to correct, corrected string as tuple below to correct an address street name entry. Ordered dictionary by length.
street_mapping = OrderedDict([('East Whitestone Blvd T100, Cedar Park, TX 78613, United States', 'East Whitestone Boulevard'), 
                              ('North Interstate Hwy 35, Round Rock, TX 78681', 'North I-35'), ('North Interstate Highway 35 Frontage Road', 'North I-35'), 
                              ('North Interstate Highway 35 Service Road', 'North I-35'), ('Louis Henna Blvd, TX 45 Frontage Road', 'Louis Henna Boulevard'), 
                              ('Interstate Highway 35 Frontage Road', 'I-35'), ('Pecan Park Ste 300, Cedar Park, TX', 'Pecan Park Boulevard'), 
                              ('Interstate Highway 35 Service Road', 'I-35'), ('East Whitestone Blvd Ste G-145', 'East Whitestone Boulevard'), 
                              ('State Highway 45 Frontage Road', 'SH 45'), ('South Interstate Highway 35', 'South I-35'), 
                              ('South Bell Blvd, Suite 301', 'South Bell Boulevard'), ('South Interstate 35, #260', 'South I-35'), 
                              ('Ranch-to-Market Road 620', 'Ranch Road 620'), ('North IH 35 Pflugerville', 'North I-35'), 
                              ('North Interstate Hwy 35', 'North I-35'), ('Highway Interstate 35', 'I-35'), ('TX 130 Frontage Road', 'North State Highway 130'), 
                              ('North I-35 Suite 298', 'North I-35'), ('North Interstate 35', 'North I-35'), ('South Interstate 35', 'South I-35'), 
                              ('North FM 620 Bldg 2', 'North Farm to Market 620'), ('183A Frontage Road', '183A Toll Road'), ('North Highway 183', 'North US 183'), 
                              ('Highway 183 North', 'North US 183'), ('Raglan CastlePath', 'Raglan Castle Path'), ('Monarch Butterfly', 'Monarch Butterfly Way'), 
                              ('University Blvd', 'University Boulevard'), ('North SH 130 NB', 'North State Highway 130'), ('Murchison Ridge', 'Murchison Ridge Trail'), 
                              ('Caisteal Castle', 'Caisteal Castle Path'), ('Ranch Rd 620 N', 'North Ranch Road 620'), ('Mellow Meadows', 'Mellow Meadows Drive'), 
                              ('US Highway 183', 'US 183'), ('Brown Juniper', 'Brown Juniper Way'), ('North Hwy 183', 'North US 183'), 
                              ('North FM 620', 'North Farm to Market 620'), ('Canyon Maple', 'Canyon Maple Drive'), ('Royal Dublin', 'Royal Dublin Drive'), 
                              ('FM 620 North', 'North Farm to Market 620'), ('North Sh 130', 'North State Highway 130'), ('North RM 620', 'North Ranch Road 620'), 
                              ('Royal Pointe', 'Royal Pointe Drive'), ('North I -35', 'North I-35'), ('North IH-35', 'North I-35'), ('North IH35,', 'North I-35'), 
                              ('IH 35 North', 'North I-35'), ('North IH 35', 'North I-35'), ('Stonebridge', 'Stonebridge Drive'), ('Canterwood', 'Canterwood Lane'), 
                              ('North IH35', 'North I-35'), ('South IH35', 'South I-35'), ('Trail Dust', ' Trail Dust Drive'), ('Crossings', 'Crossing'), 
                              ('Edenderry', 'Edenderry Drive'), ('MCNEIL RD', 'McNeil Road'), ('Barrhead', 'Barrhead Cove'), ('Talamore', 'Talamore Road'), 
                              ('Buckskin', 'Buckskin Drive'), ('St Marys', "St Mary's Drive"), ('Dalmahoy', 'Dalmahoy Drive'),('U.S. 183', 'US 183'), ('FM 1325', 'Farm to Market 1325'), 
                              ('Casitas', 'Casitas Drive'), ('FM 1460', 'Farm to Market 1460'), ('RM 620', 'Ranch Road 620'), ('FM 685', 'Farm to Market 685'), 
                              ('RR 620', 'Ranch Road 620'), ('IH35,', 'I-35'), ('US-79', 'US 79'), ('North', ''), ('IH-35', 'I-35'), ('South', ''), ('West', ''), 
                              ('Toll', 'Toll Road'), ('IH35', 'I-35'), ('East', ''), ('pass', 'Pass'), ('Blvd', 'Boulevard'), ('Trl', 'Trail'), ('Ave', 'Avenue'), 
                              ('Cv', 'Cove'), ('NB', ''), ('Rd', 'Road'), ('Dr', 'Drive'), ('St', 'Street')
                              ])


# Catch streetname ending in Frontage Road or Service Road
special_streetname_substrings = ["Frontage", "Service"]


# ************************* not_special_street() called from update_street() *************************

def not_special_street(street_name):
    """Filter out streetname ending in Frontage Road or Service Road."""
    not_special = not any([substring in street_name for substring in special_streetname_substrings])
    return not_special



# ************************* preprocess_streetname() called from update_street()*************************

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



# ************************* update_street() *************************

def update_street(street_name):
    """Update streetname record to consistent format pattern.

    Takes in a street name as a string.
    Returns corrected streetname as string.
    
    Checks street_name against street_mapping
    dictionary and starts/ends with digit. Updates and returns street name if in 
    street_mapping or returns if in expected_street_list or end_in_number set.
    """

    # if (street_name[-1].isdigit()) and (street_name in end_in_number):
    #     return street_name

    street_name = preprocess_streetname(street_name)

    m = street_type_re.search(street_name)  

    if m:                                                                   
        street_type = m.group()
        if (street_type in expected_street_list) and (not_special_street(street_name)):
            return street_name

        for key in street_mapping.keys():
            if street_name.endswith(key):
                street_name =street_name.replace(key, street_mapping[key])
                return street_name
  
    return street_name
