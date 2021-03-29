#!/usr/bin/env python
"""Functions used to explore data."""

import xml.etree.cElementTree as ET
import re

import pprint

# *******************NOT USED  get_root() *************************

def get_root(OSM_FILE = "data\\round_rock.xml"):
  """Takes in .osm or .xml file and returns root tag. """
  
  tree = ET.parse(OSM_FILE)
  root = tree.getroot()
  print(root.tag)
  return root.tag


#************************* count_tags() *************************

def count_tags(OSM_FILE = "data\\round_rock.xml"):
  """Takes in .osm or .xml file and returns a dictionary 
      of each root tag as key with count of each 
      root tag found as value.

      Use Case:
        tag_dict = count_tags(OSM_FILE)
        pprint.pprint(tag_dict)
  """
  tags = {}

  for event, elem in ET.iterparse(OSM_FILE):
      if elem.tag not in tags:
          tags[elem.tag] = 1

      else:
          tags[elem.tag] = tags[elem.tag] + 1

  return tags


#************************* categorize_tag_key_characters() *************************

def categorize_tag_key_characters(OSM_FILE = "data\\round_rock.xml", category = 'Summary'):
  """Categorizes attributes into those with:
        all lower character, all lower after colon(:),
        containing special/problem characters and 
        all all others that were not listed in above
          which includes uppercase characters and/or 
          multiple colons.

  Keyword arguments:
  OSM_File -- .osm or .xml file (default "data\\round_rock.xml")
  category  -- print specific keys of categories of characters from regex search
                (default 'Summary' ['All', 'lower', 'lower_colon', 'porblemchars', 'other'])
  """
  if category == 'All':
    category = ('lower', 'lower_colon', 'porblemchars', 'other')

  category_list = list(category)

  lower = re.compile(r'^([a-z]|_)*$')
  lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
  problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

  lower_set = set()
  lower_colon_set = set()
  problemchars_set = set()
  other_set = set()

  def key_type(element, keys):
      if element.tag == "tag":
          
          if lower.match(element.attrib['k']):
              lower_set.add(element.attrib['k'])
              keys["lower"] += 1
          elif lower_colon.match(element.attrib['k']):
              lower_colon_set.add(element.attrib['k'])
              keys["lower_colon"] += 1
          elif problemchars.match(element.attrib['k']):
              problemchars_set.add(element.attrib['k'])
              keys["problemchars"] += 1
          else:
              other_set.add(element.attrib['k'])
              keys["other"] += 1
      return keys

  def process_map(filename):
      keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
      for _, element in ET.iterparse(filename):
          keys = key_type(element, keys)
      
      print(keys)
      print(
        "\nThere are:\n\
          {} unique keys in lower,\n\
          {} unique keys in lower_colon,\n\
          {} unique keys in problemchars and\n\
          {} unique keys in other.\n"
          .format(len(lower_set), len(lower_colon_set), len(problemchars_set), len(other_set))
      )

      if 'lower' in category_list: 
        print('\n\nlower set has {} items. The unique items are: \n\n{} \n\n'
        .format(keys["lower"], sorted(lower_set)))
      if 'lower_colon' in category_list: 
        print('lower_colon set has {} items. The unique items are: \n\n{} \n\n'
        .format(keys["lower_colon"], sorted(lower_colon_set)))
      if 'problemchars' in category_list: 
        print('problemchars set has {} items. The unique items are: \n\n{} \n\n'
        .format(keys["problemchars"], sorted(problemchars_set)))
      if 'other' in category_list: 
        print('other set has {} items. The unique items are: \n\n{} \n\n'
        .format(keys["other"], sorted(other_set)))

      return keys

  keys_dicts = process_map(OSM_FILE)
  return keys_dicts


# *******************  distinct_users()  *************************

def distinct_users(OSM_FILE = "data\\round_rock.xml"):
  """Takes in .osm or .xml file and return dictionary of distinct uid : user k-v pairs."""

  users = {}
  for not_used, element in ET.iterparse(OSM_FILE):
      if element.tag in ['node', 'way', 'relation']:
          users[element.attrib['uid']] = element.attrib['user']

  print("There are {} distinct users who have contributed data.".format(len(users)))
  return users





