# Data Wrangling Project using OSM data set

### This is an academic project for a Data Wrangling course using the OpenStreetMaps data source.

File Descriptions and Layout of Files:

**Updates and Changes from Previous Submission** 03/17/21

All the three audit files in the module folder are scripts with **data\\round_rock_sample.xml as the default**.
The **audits.py** script file will run all audit functions.

**data.py to a script file** uses **data\\round_rock_sample.xml as the default** with **validate set to false**.

**audits.py** holds all auditing functions and can be run as a script file.

**explore_data.py** script file runs the data explore functions successively.

**converted the Python 2 code to Python 3**
Changes are: 
- changed the open() calls to with open(), 
- the iteritems() to items()
- changed the isinstance(v, unicode) to a encoding = 'utf-8' parameter in the codec.open and
- modified some of the previous codes imports and flow to accomadate a script call versus a function call.
    
After completing these steps, the code **no longer is able to run in Python 2.7**. The code does
run in Python 3 and the timing have improved significantly.

The remaining items below are from initial completion. 

The **PCook_DW_OpenStreetMaps.html** file contains the write up and answers to the rubric questions.
There are active highlighted links to both, Folders and Python Code files references, and all links will open in a new tab/window.
The functions within the .py files have a comment header ( # **** function_name() ****) to help find/identify the function. In addition the functions contain docstrings.

The **PCook_With_Code_DW_OpenStreetMaps.ipynb** file contains the same information as the file above but contains the working code (versus markdown) following the text if testing is needed.

The **PCook_Markdown_DW_OpenStreetMaps.ipynb** file is the source file of the html file and contains
    the same information with no working code (all Markdown).

The **data folder** holds the 3 osm (xml) files used:
- ~~round_rock.xml              Complete file 220 MB~~ (must download due to size)
- round_rock_sample.xml       ~10 MB sample file
- test.xml                    Used for testing specific problem nodes and schema

The **Images folder** holds 1 image used in the report.

The **modules** hold all the .py files for the functions used.
    The functions are grouped into audit files, helper files, and update (cleaning) files.
    The update_values.py file is used for flow control for the cleaning functions.
        example (street key; value goes to --> update_streets.py)

The **sql folder** holds the database file (Round_RockDb.db) and all the csv files.
    There is a copy of the create_table_schema in this folder for convenience.

**data.py** holds the modified data.py code (conversion to Python 3) with cleaning steps added.

**schema.py** is used for cerberus (**See important Note Below**)
    cerberus was used to validate the entire dataset before submission.
    **It will take over an hour to run on a professional workstation** and
      is therefore set to false in the jupyter "With_Code" file.


### Future Tasks:
* reduce/compress code duplication
* move reusable functions into utility helper module and generalize naming
* expand on analysis of business using distance/position from major roadways
* query businesses with missing information such as phone/hours/etc...
* use external db to determine businesses not listed in the dataset (contact for inclusion)

