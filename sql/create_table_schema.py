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