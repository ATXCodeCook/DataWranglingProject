#!/usr/bin/env python
"""SQL helper functions and SQL statements"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import pprint

# db_file = 'sql\\Round_RockDb.db'

create_tables = ["""DROP TABLE IF EXISTS nodes;""",
                
                """
                CREATE TABLE IF NOT EXISTS nodes (
                    id INTEGER PRIMARY KEY,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    user TEXT NOT NULL,
                    uid INTEGER NOT NULL,
                    version TEXT NOT NULL,
                    changeset INTEGER NOT NULL,
                    timestamp DATE NOT NULL
                );""",

                """DROP TABLE IF EXISTS nodes_tags;""",

                """
                CREATE TABLE IF NOT EXISTS nodes_tags (
                    id INTEGER NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    type TEXT NOT NULL,
                    FOREIGN KEY (id) REFERENCES nodes (id),
                    FOREIGN KEY (id) REFERENCES ways_nodes (node_id)
                );""",

                """DROP TABLE IF EXISTS ways;""",

                """
                CREATE TABLE IF NOT EXISTS ways (
                    id INTEGER PRIMARY KEY,
                    user TEXT NOT NULL,
                    uid INTEGER NOT NULL,
                    version TEXT NOT NULL,
                    changeset INTEGER NOT NULL,
                    timestamp DATE NOT NULL
                );""",

                """DROP TABLE IF EXISTS ways_nodes;""",

                """               
                CREATE TABLE IF NOT EXISTS ways_nodes (
                    id INTEGER NOT NULL,
                    node_id INTEGER NOT NULL,
                    position INTEGER NOT NULL,
                    FOREIGN KEY (id) REFERENCES ways (id),
                    FOREIGN KEY (node_id) REFERENCES nodes (id)
                );""",

                """DROP TABLE IF EXISTS ways_tags;""",
                
                """
                CREATE TABLE IF NOT EXISTS ways_tags (
                    id INTEGER NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    type TEXT NOT NULL,
                    FOREIGN KEY (id) REFERENCES ways (id),
                    FOREIGN KEY (id) REFERENCES ways_nodes (node_id)
                );"""
                ]

# ***********************************************************************
# *                                                                     *
# *                            Helper Functions                         *
# *                                                                     *
# ***********************************************************************


def create_connection(db_file):
    """Create database connection to SQLite database with error handling.
    
    Keyword arguments:
    db_file -- string file path to database
    """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print("Db Open:  SQLite3 version {}".format(sqlite3.version))
        return conn

    except Error as e:
        print(e)

def close_connection(conn):
        print('Closing Db connection')
        if conn:
            conn.close()
            print("Connection closed.\n")



# ************************* process_sql() *************************

def process_sql(db_file, sql_statement, commit_change = False, print_output = False):
    """ Process SQLite3 SQL statements given in create_table_sql
    
    Keyword arguments:
    db_file -- string:string file path to database
    sql_statement -- string: sql_statement to execute
    commit_change -- Bool: commit sql statement (default False)
    print_output  -- Bool: print query results (default False; __main__ default True)
    """
    conn = create_connection(db_file)
    output = ''

    if conn is not None:

        try:
            c = conn.cursor()
            output = c.execute(sql_statement).fetchall()

            if commit_change == True:
                c.execute('COMMIT;')

        except Error as e:
            print("\nThe statement\n {}\n\nfailed to execute with the Error:  {}\n"\
                  .format(sql_statement, e))
            print
    

    else:
        print("Error! Failed to create database connection.")
    c.close()
    close_connection(conn)

    if print_output:
        pprint.pprint(output)
    
    if not print_output:
        return output


# ************************* csv_to_sql() *************************

def csv_to_sql(csv_file_path, db_file, db_table):
    """ Converts csv file to sql table based on csv header for column insertion.
    
        Keyword arguments:
        csv_file_path -- string file path to csv file
        db_file -- string file path to database
        table_name -- name of table to insert into

        Note, if the table does not exist, tables should be created using 
        appropriate schema before converting csv to sql.
    """
    table_name = db_table
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    csv_file = pd.read_csv(csv_file_path)
    print("\nProcessing {} file to {} table.".format(csv_file_path, db_table))

    csv_file.to_sql(table_name, conn, if_exists='append', index = False)
    
    close_connection(conn)



# ************************* sql_query() *************************

def sql_query(db_file, sql_statement, print_output = True):

    conn = sqlite3.connect(db_file)
    output = pd.read_sql_query(sql_statement, conn, index_col = None)
    if print_output:
        print(output)
    
    if not print_output:
        return output

if __name__ == "__main__":
    process_sql(db_file = 'sql\Round_RockDb.db', 
                sql_statement = 'SELECT * FROM nodes_tags ' \
                                'WHERE key = "street" LIMIT 10;',
                print_output = True)