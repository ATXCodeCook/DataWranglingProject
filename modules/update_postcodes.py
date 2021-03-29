#!/usr/bin/env python
"""Update postcodes using mapping dictionary."""

postcode_mapping = {'78621' : '78681', '787664' : '78664', '78728-1275' : '78728'}


# ************************* update_postcode() *************************

def update_postcode(postcode_value):
    """Takes postcode value, updates using postcode_mapping
    dictionary and returns updated value.
    """
    if postcode_value not in postcode_mapping.keys():
        return postcode_value
    else:
        return(postcode_mapping[postcode_value])
