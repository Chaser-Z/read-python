#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import mysql.connector

def read_db_config():
    config = configparser.ConfigParser()
    config.read('db.cnf')
    host = config.get('mysql', 'host')
    port = config.get('mysql', 'port')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    database = config.get('mysql', 'database')
    return host, port, user, password, database

_host, _port, _user, _password, _database = read_db_config()



def check_and_create_database():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database='mysql')
    cursor = conn.cursor()
    sql = 'select count(*) from information_schema.schemata where schema_name=%s;'
    cursor.execute(sql, [_database])
    values = cursor.fetchall()
    result = values[0][0]

    if result == 0:
        sql = 'create database %s;' % _database
        cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()
    return True if result == 1 else False


def create_tables():
    sql_path = 'read_crawler_table.sql'
    with open(sql_path, 'r') as sql_file:
        sql = sql_file.read()
        sql_file.close()
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    for result in cursor.execute(sql, multi=True):
        pass
    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()


def do_work():
    has_db = check_and_create_database()
    if has_db:
        print("Found existing database %s, tables are not created!" % _database)

    else:
        create_tables()
        print("Database %s and tables are created." % _database)

if __name__ == '__main__':
    do_work()
    print('01_prepare_db.py done')