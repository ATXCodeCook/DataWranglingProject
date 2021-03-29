#!/usr/bin/env python


"""Flow control and processing for cleaning and converting
xml data to csv data. The csv files are stored in the
sql_imports folder.

Note the cerberus validation will cause the routine to take
a considerable amount of time. If it is a concern, comment out
the four lines indicated with comments or set validate=False in
the process_map function at the bottom of this file.

"""

import csv
import codecs
import re
import xml.etree.cElementTree as ET
from collections import OrderedDict

import cerberus                                                 # Comment out this line if cerberus not installed.
import pprint

import schema
from modules.update_values import update_value

# OSM_FILE = "data\\round_rock.xml" # set as default in fucntion


# ********************************** xml_to_csv() ***********************************

def xml_to_csv(OSM_FILE = "data\\round_rock.xml", validate = False):

    NODES_PATH = "sql\\csv\\nodes.csv"
    NODE_TAGS_PATH = "sql\\csv\\nodes_tags.csv"
    WAYS_PATH = "sql\\csv\\ways.csv"
    WAY_NODES_PATH = "sql\\csv\\ways_nodes.csv"
    WAY_TAGS_PATH = "sql\\csv\\ways_tags.csv"

    LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
    PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

    SCHEMA = schema.schema

    # Make sure the fields order in the csvs matches the column order in the sql table schema
    NODE_FIELDS_list = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
    NODE_TAGS_FIELDS_list = ['id', 'key', 'value', 'type']
    WAY_FIELDS_list = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
    WAY_TAGS_FIELDS_list = ['id', 'key', 'value', 'type']
    WAY_NODES_FIELDS_list = ['id', 'node_id', 'position']

    NODE_FIELDS = set(NODE_FIELDS_list)
    NODE_TAGS_FIELDS = set(NODE_TAGS_FIELDS_list)
    WAY_FIELDS = set(WAY_FIELDS_list)
    WAY_TAGS_FIELDS = set(WAY_TAGS_FIELDS_list)
    WAY_NODES_FIELDS = set(WAY_NODES_FIELDS_list)

    # List of tag.attrib key values to update
    UPDATE_LIST = ['addr:street', 'addr:postcode', 'phone']

    def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                    problem_chars=PROBLEMCHARS, default_tag_type='regular'):
        """Clean and shape node or way XML element to Python dict"""

        node_attribs = {}
        way_attribs = {} 
        way_nodes = []
        tags = []

        # Start of data element processing
        if element.tag == 'node':
            for key in NODE_FIELDS:
                node_attribs[key] = element.attrib[key]

            for child in element.iter('tag'):
                tag_dict = {}

                if child.attrib['k'] in UPDATE_LIST:                                        
                    child.attrib['v'] = update_value(child.attrib['k'], child.attrib['v'])  # Cleaning called here by calling update_value for nodes

                tag_key = child.attrib['k']
                tag_val = child.attrib['v']          
                tag_type = 'regular'

                if ':' in tag_key:
                    split_key = tag_key.split(':', 1)
                    tag_type = split_key[0]
                    tag_key = split_key[1]
                
                tag_dict['id'] = element.attrib['id']
                tag_dict['key'] = tag_key
                tag_dict['value'] = child.attrib['v']   
                tag_dict['type'] = tag_type    

                tags.append(tag_dict)

            return {'node': node_attribs, 'node_tags': tags}

        elif element.tag == 'way':
            for key in WAY_FIELDS:
                way_attribs[key] = element.attrib[key]

            for child in element.iter('tag'):
                tag_dict = {}

                if child.attrib['k'] in UPDATE_LIST:                                        
                    child.attrib['v'] = update_value(child.attrib['k'], child.attrib['v'])  # Cleaning called here by calling update_value for ways

                tag_key = child.attrib['k']
                tag_val = child.attrib['v']          
                tag_type = 'regular'

                if ':' in tag_key:
                    split_key = tag_key.split(':', 1)
                    tag_type = split_key[0]
                    tag_key = split_key[1]
                
                tag_dict['id'] = element.attrib['id']
                tag_dict['key'] = tag_key
                tag_dict['value'] = child.attrib['v']
                tag_dict['type'] = tag_type    

                tags.append(tag_dict)
        

            for position, child in enumerate(element.iter('nd')):
                node_dict = {}

                node_dict['id'] = element.attrib['id']
                node_dict['node_id'] = child.attrib['ref']
                node_dict['position'] = position

                way_nodes.append(node_dict)

            return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

    # ================================================== #
    #               Helper Functions                     #
    # ================================================== #
    def get_element(osm_file, tags=('node', 'way', 'relation')):
        """Yield element if it is the right type of tag"""

        context = ET.iterparse(osm_file, events=('start', 'end'))
        _, root = next(context)
        for event, elem in context:
            if event == 'end' and elem.tag in tags:
                yield elem
                root.clear()

    def validate_element(element, validator, schema=SCHEMA):
        """Raise ValidationError if element does not match schema"""
        if validator.validate(element, schema) is not True:
            field, errors = next(validator.errors.items())
            message_string = "\nElement of type '{0}' has the following errors:\n{1}\n{}"

            error_string = pprint.pformat(errors)
            print("***ERROR around element: \n {}".format(element))

            raise Exception(message_string.format(field, error_string))

    class UnicodeDictWriter(csv.DictWriter, object):
        """Extend csv.DictWriter to handle Unicode input"""

        def writerow(self, row):
            super(UnicodeDictWriter, self).writerow({
                # Removed dated/depricated code.
                # k: (v.encode('utf-8') if isinstance(v, bytes) else v) for k, v in row.items()
                k: v for k, v in row.items()
            })

        def writerows(self, rows):
            for row in rows:
                self.writerow(row)

    # ================================================== #
    #               Main Function                        #
    # ================================================== #
    def process_map(file_in, validate):
        """Iteratively process each XML element and write to csv(s)"""

        with codecs.open(NODES_PATH, 'wb', encoding = 'utf-8') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'wb', encoding = 'utf-8') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'wb', encoding = 'utf-8') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'wb', encoding = 'utf-8') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'wb', encoding = 'utf-8') as way_tags_file:

            nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
            node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
            ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
            way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
            way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

            nodes_writer.writeheader()
            node_tags_writer.writeheader()
            ways_writer.writeheader()
            way_nodes_writer.writeheader()
            way_tags_writer.writeheader()

            validator = cerberus.Validator()                        

            for element in get_element(file_in, tags=('node', 'way')):
                el = shape_element(element)
                if el:
                    if validate is True:                            
                        validate_element(el, validator)             

                    if element.tag == 'node':
                        nodes_writer.writerow(el['node'])
                        node_tags_writer.writerows(el['node_tags'])
                    elif element.tag == 'way':
                        ways_writer.writerow(el['way'])
                        way_nodes_writer.writerows(el['way_nodes'])
                        way_tags_writer.writerows(el['way_tags'])


    print("Started")
    process_map(OSM_FILE, validate)                       
    print("**** Completed. Check sql/csv folder for csv files. ****")

if __name__ == "__main__":
    xml_to_csv(OSM_FILE = 'data\\round_rock_sample.xml', validate = False)
