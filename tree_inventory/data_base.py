#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:54:08 2019

@author: abdoul
"""

from psycopg2 import (
        connect
)

cleanup = (
        'DROP TABLE IF EXISTS blog_user CASCADE',
        'DROP TABLE IF EXISTS tree_data',
        'DROP TABLE IF EXISTS post'
        )

commands = (
        """
        CREATE TABLE blog_user (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) UNIQUE NOT NULL,
            user_password VARCHAR(255) NOT NULL
        )
        """,
         """ 
        CREATE TABLE tree_data (
                dataid SERIAL PRIMARY KEY,
                author INTEGER NOT NULL,
                creation TIMESTAMP DEFAULT NOW(),
                kind VARCHAR(255) NOT NULL,
                dep VARCHAR(255) NOT NULL,
                circumference VARCHAR(255) NOT NULL,
                height VARCHAR(255) NOT NULL,
                latitude VARCHAR(255) NOT NULL,
                longitude VARCHAR(255) NOT NULL,
                FOREIGN KEY (author)
                    REFERENCES tree_data (dataid)
        )
        """,
        """ 
        CREATE TABLE post (
                post_id SERIAL PRIMARY KEY,
                author_id INTEGER NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                title VARCHAR(350) NOT NULL,
                body VARCHAR(500) NOT NULL,
                FOREIGN KEY (author_id)
                    REFERENCES blog_user (user_id)
        )
        """)

sqlCommands = (
        'INSERT INTO blog_user (user_name, user_password) VALUES (%s, %s) RETURNING user_id',
        'INSERT INTO tree_data (longitude,latitude,kind, dep, circumference, height, author) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        'INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)'
        )        
conn = connect("dbname=postgres user=postgres password=Kassim123*")
cur = conn.cursor()
for command in cleanup :
    cur.execute(command)

for command in commands :
    cur.execute(command)

cur.execute(sqlCommands[0], ('Abdoul', '3ety3e7'))
userId = cur.fetchone()[0]
#cur.execute(sqlCommands[1], ('My First Post', 'This is the post body', userId))
#cur.execute('SELECT * FROM post')
cur.execute(sqlCommands[1], ('Honey Locust', '8','30','120','29.05','-81.705', userId))
cur.execute(sqlCommands[1], ('Buckeye', '0','35','120','41.045','-86.60', userId))
cur.execute(sqlCommands[1], ('Cotton wood', '10','20','90','41.06','-86.62', userId))
cur.execute(sqlCommands[2], ('Please!', 'leave a comment', userId))

#print(cur.fetchall())

cur.close()
conn.commit()
conn.close()
