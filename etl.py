import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
import time


def load_staging_tables(cur, conn):
    """
    Loads data into staging tables which are defined in 
    copy_table_queries LIST located in sql_queries.py file. 

    Args:
        cur: The database cursor.
        conn: The database connection.

    Returns:
        None
    """
    for query in copy_table_queries:
        table_name = query[0:27].splitlines()[1]
        print("{} ...".format(table_name))

        start_time = time.time()
        cur.execute(query)
        end_time = time.time()

        execution_time = end_time - start_time
        print("Done in {:.2f} seconds".format(execution_time))

        conn.commit()


def insert_tables(cur, conn):
    """
    Inserts data into star schema tables which are defined in 
    insert_table_queries LIST located in sql_queries.py file. 

    Args:
        cur: The database cursor.
        conn: The database connection.

    Returns:
        None
    """

    for query in insert_table_queries:
        table_name = query[0:40].split("(")[0]
        print("{}...".format(table_name))

        start_time = time.time()
        cur.execute(query)
        end_time = time.time()

        execution_time = end_time - start_time
        print("Done in {:.2f} seconds".format(execution_time))

        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
