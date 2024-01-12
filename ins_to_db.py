#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

con = sqlite3.connect('/home/chin/Dropbox/reanW/db.sqlite3')	
cur = con.cursor()
for ff in open('/home/chin/Dropbox/reanW/res/texts/main.txt').readlines():
    if ff !='' and len(ff.split(';')) > 4:
        cur.execute("INSERT INTO rean_rean (title_file,  title_dif, title_th, title_ru, title_is, text_note, text_ph, text_ex, created_date, published_date, author_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ff.split(';')[0], ff.split(';')[5].replace('\n', ''), ff.split(';')[1], ff.split(';')[2], '*', ff.split(';')[4], '*', '*', '2024-01-09 10:37:44.927280', '', 1))
con.commit()
cur.close()
con.close() 


#conM = pymysql.connect(host="138.201.127.82", user="paradiseremote", \
                #passwd="39xIQC9ho5LrsfYo", db="rabopoffice", charset='utf8')
#CREATE TABLE "rean_rean" (
	#"id"	integer NOT NULL,
	#"title_file"	varchar(200) NOT NULL,
	#"title_dif"	varchar(4) NOT NULL,
	#"title_th"	varchar(200) NOT NULL,
	#"title_ru"	varchar(200) NOT NULL,
	#"title_is"	varchar(200) NOT NULL,
	#"text_note"	text NOT NULL,
	#"text_ph"	text NOT NULL,
	#"text_ex"	text NOT NULL,
	#"created_date"	datetime NOT NULL,
	#"published_date"	datetime,
	#"author_id"	integer NOT NULL,
	#PRIMARY KEY("id" AUTOINCREMENT),
	#FOREIGN KEY("author_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
