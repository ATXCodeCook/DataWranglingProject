#!/usr/bin/env python
""" audits(OSM_FILE = "data\\round_rock.xml") runs
    the functions used to explore the data.

    The following functions will be run and results printed:
        _ = count_tags(OSM_FILE)
        _ = categorize_tag_key_characters(OSM_FILE)
        _ = distinct_users(OSM_FILE)

"""
from modules.audit_streets import audit_street_validate_corrections
from modules.audit_postcodes import audit_postalcode
from modules.audit_phones import audit_phones
from modules.helper_functions import phone_partial_clean


def audits(OSM_FILE):
    print('\nUsing round_rock_sample.xml file\n')
    print('**** Audit Streets: \n')
    audit_street_validate_corrections(OSM_FILE = "data\\round_rock_sample.xml")
    print('\n\n')
    print('**** Audit Postcodes: \n')
    postcode_problems = audit_postalcode(OSM_FILE = "data\\round_rock_sample.xml")
    print('\n\n')
    print('**** Audit Phones')
    malform_numbers = audit_phones(OSM_FILE = "data\\round_rock_sample.xml")
    print('\nPartial Cleaning of Phone Numbers: \n')
    new_phone_to_clean_map = phone_partial_clean(malform_numbers)
    print('\n\n Audits complete.\n')


if __name__ == "__main__":
    audits(OSM_FILE = "data\\round_rock_sample.xml")