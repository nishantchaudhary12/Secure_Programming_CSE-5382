# python 3.5.2

import sqlite3
from sqlite3 import Error
import re


def check_name(name_string):
    test_name = name_regex_pattern.match(name_string)
    if test_name:
        return True
    else:
        return False


def check_phone(number_string):
    test_number = phone_number_regex_pattern.match(number_string)
    if test_number:
        return True
    else:
        return False


def create_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    try:
        conn = sqlite3.connect(':memory:')

        # create members table
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS members (
                                                    id integer PRIMARY KEY,
                                                    name text NOT NULL,
                                                    phone text NOT NULL
                                                ); """

        if conn is not None:
            # create projects table
            try:
                c = conn.cursor()
                c.execute(sql_create_projects_table)
            except Error as err:
                print(err)

        return conn
    except Error as e:
        print(e)

    return None


def add_member(conn, name, phone):
    if conn is not None:
        values_to_insert = [(name, phone)]
        # query = "INSERT INTO members (name, phone) VALUES ('" + name + "','" + phone + "');"
        cur = conn.cursor()
        # cur.execute(query)
        cur.executemany("""
            INSERT INTO members ('name', 'phone')
            VALUES (?, ?)""", values_to_insert)


def list_members(conn):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")

        for row in cur:
            print(row)
        # rows = cur.fetchall()
        #
        # for row in rows:
        #     print(row)
    else:
        print("DB connection error!")


def delete_member(conn, value):
    if conn is not None:
        cur = conn.cursor()
        if cur.execute("DELETE FROM members WHERE name = '" + value + "' OR phone = '" + value + "';"):
            print("successfully deleted")
        else:
            print("Not a valid record")


def regex_check(conn):
    # if conn is not None:
    user_input = input("Enter Command:")
    # user_input = 'ADD "Nishant" "12345.12345"'
    user_command = user_input.split('"')
    user_command = [e.strip() for e in user_command if e not in (' ', '')]
    print(user_command)
    if user_command[0] == "LIST":
        print("##### List Command #####")
        list_members(conn)
    elif user_command[0] == "DEL":
        print("##### Delete Command #####")
        np = user_command[1]
        delete_member(conn, np)
    elif user_command[0] == "ADD":
        print("###### Add Command #####")
        if len(user_command) == 3:
            name = user_command[1]
            phone = user_command[2]
            print(name, phone)
            test_name = check_name(name)
            test_phone = check_phone(phone)

            if test_name:
                if test_phone:
                    print(test_phone)
                    add_member(conn, name, phone)
                else:
                    print("invalid phone number")
                    print("print help e.g. <executable name> <mode> <arguments>")
            else:
                print("invalid name")
        else:
            print("Please check your command. \n valid command e.g. <executable name> <mode> <arguments>")
    else:
        print("Not a valid command!")
        print("print help e.g. <executable name> <mode> <arguments>")

        print("""
                • ADD “<Person>” “<Telephone #>” - Add a new person to the database
                • DEL “<Person>” - Remove someone from the database by name
                • DEL “<Telephone #>” - Remove someone by telephone #
                • LIST - Produce a list of the members of the database
                """)


if __name__ == '__main__':
    # regular expression for validating name
    name_regex_string = "^[A-Z]\\'?([a-zA-Z]*?\\'?[a-zA-Z]*?\\,?[ ]?\\'?\\-?\\.?){1,3}$"
    name_regex_pattern = re.compile(name_regex_string)

    # regular expression for validating phone#
    phone_number_regex_string = "(^\\d{5}$)|(^\\d{5}\\.\\d{5}$)|(^\\+[1-9]{1,2}[ ]?\\(|^[1][ ]?\\(|^[0][1][1][ ][1]?[ " \
                                "]?\\(?|^\\(?)([1-9]\\d{1,2})?\\)?[- ]?(\\d{3})[-| ](\\d{4})$";
    phone_number_regex_pattern = re.compile(phone_number_regex_string)
    conn = create_connection()

    while True:
        regex_check(conn)
