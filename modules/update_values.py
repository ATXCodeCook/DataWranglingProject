#!/usr/bin/env python
"""Takes strings from tag attribute key and value. 
Sends value to correct update function based on 
key and returns updated value to calling function
in data.py.
"""

from modules.update_streets import update_street
from modules.update_postcodes import update_postcode
from modules.update_phones import update_phone


update_errors_dict = {}


# ************************* update_value() *************************

def update_value(attrib_key, attrib_val):
    """Call specific update function based on tag.attrib key and return updated value."""
    
    if attrib_key == 'addr:street':
        attrib_val = update_street(attrib_val)
    
    elif attrib_key == 'addr:postcode':
        attrib_val = update_postcode(attrib_val)

    elif attrib_key == 'phone':
        attrib_val = update_phone(attrib_val)

    else:
        print("Missed value: check update_errors_dict")
        update_errors_dict[attrib_key] = attrib_val

    return attrib_val