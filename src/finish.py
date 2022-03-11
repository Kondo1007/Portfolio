#!/usr/bin/python3
# -*- coding: UTF-8 -*-


def print_header():
    print("<head>")
    print("<link rel=\"stylesheet\" href=\"https://cdn.datatables.net/t/bs-3.3.6/jqc-1.12.0,dt-1.10.11/datatables.min.css\"/>")
    print("<script src=\"https://cdn.datatables.net/t/bs-3.3.6/jqc-1.12.0,dt-1.10.11/datatables.min.js\"></script>")
    print("<script>")
    print("    jQuery(function($){$(\"#res-table\").DataTable();});")
    print("</script>")
    print("<title>Event search results</title>")
    print("</head>")

def save_db(ipaddr, tai, name):
    import sqlite3
    from contextlib import closing
    
    dbname = '/var/www/db/access3.db'
    
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = '''create table if not exists access (id integer primary key, ipaddr varchar(16), tai varchar(5), name varchar(30), updated datetime)'''
        c.execute(create_table)
        sql = 'insert into access (ipaddr, tai, name, updated) values (?,?,?,?)'
        import datetime
        access = (ipaddr, ','.join(tai), ','.join(name), datetime.datetime.now())
        c.execute(sql, access)
        conn.commit()
        conn.close()

import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if ( os.environ['REQUEST_METHOD'] == "GET" ):
    import requests, urllib
    form = urllib.parse.parse_qs(os.environ['QUERY_STRING'])
    tai = form['tai'] if 'tai' in form else []
    name = form['name'] if 'name' in form else []
    print('Content-Type:text/html\n')
    print("<html lang=\"ja\">")
    if (float(tai[0]) >= 37.5):
        print("入場出来ません．担当者に報告お願いします.")
    if (float(tai[0]) <= 37.4):
        print("保存しました．")
    print("</tbody></table>")
    print("</body></html>") 
    save_db(os.environ['REMOTE_ADDR'], tai, name)

