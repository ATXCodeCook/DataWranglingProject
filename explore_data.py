#!/usr/bin/env python
""" explore_data(OSM_FILE = "data\\round_rock.xml") runs
    the functions used to explore the data.

    The following functions will be run and results printed:
        _ = count_tags(OSM_FILE)
        _ = categorize_tag_key_characters(OSM_FILE)
        _ = distinct_users(OSM_FILE)


"""
from modules.explore_raw_data import count_tags, categorize_tag_key_characters, distinct_users

def explore_data(OSM_FILE = "data\\round_rock.xml"):

    print("\nTag Counts:\n")
    tag_counts = count_tags(OSM_FILE)
    print(tag_counts)
    print("\n\nTag Key Categories:\n")
    _ = categorize_tag_key_characters(OSM_FILE)
    print("\nDistinct Users:\n")
    _ = distinct_users(OSM_FILE)

if __name__ == "__main__":
    explore_data(OSM_FILE = "data\\round_rock.xml")