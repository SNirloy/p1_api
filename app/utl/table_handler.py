"""
Cold Embers: Sadi Nirloy, Emily Ortiz, Gabriel Thompson, Thomas Zhang
Software Development
p1: API Project ft. Database
2022-12-11
Time Spent: 
"""

import sqlite3
DB_FILE="dampbathroom"

def setup():
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	c.execute("create table if not exists users(username text primary key, password text);")
	c.execute("create table if not exists bsns_rate(business_name text, location text primary key, net_rating integer);")
	c.execute("create table if not exists hotels(hotel_name text, location text primary key, close_arprt text);")
	
	db.commit()
	db.close()

def registrate(username, password):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	name_tuple = (username, )
	c.execute("select * from users where username = ?;", name_tuple)
	response = c.fetchall()
	# print(response)
	if (len(response) == 0):
		user_tuple = (username, password)
		c.execute("insert into users values (?, ?);", user_tuple)

		db.commit()
		db.close()

		return True

	db.commit()
	db.close()

	return False

def user_check(username):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	name_tuple = (username, )
	c.execute("select * from users where username = ?;", name_tuple)
	response = c.fetchone()
	if (response == None):
		db.commit()
		db.close()
		return False
	db.commit()
	db.close()
	return True

#USE ONLY AFTER USER_CHECK: THIS FOO ASSUMES USER IS IN USERS TABLE
def password_check(username, password):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	name_tuple = (username, )
	c.execute("select password from users where username = ?;", name_tuple)
	response = c.fetchone()
	if (response != None and response[0] == password):
		db.commit()
		db.close()
		return True
	db.commit()
	db.close()
	return False
	
# Adds a business if not in table. Does nothing if it is.
def add_bsns(bsns_name, bsns_place):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	place_tuple = (bsns_place, )
	c.execute("select * from bsns_rate where location = ?;", place_tuple)
	response = c.fetchone()
	if (response == None):
		bsns_tuple = (bsns_name, bsns_place)
		c.execute("insert into bsns_rate values (?, ?, 0);", bsns_tuple)

	db.commit()
	db.close()	


# Changes the rating of a business based on the given value
# ADD A BUSINESS BEFORE RATING IT
def rate_bsns(bsns_place, score_change):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	place_tuple = (bsns_place, )
	c.execute("select * from bsns_rate where location = ?;", place_tuple)
	response = c.fetchone()
	print(response)
	score = int(response[2])
	score += score_change
	bsns_tuple = (score,response[1])
	c.execute("update bsns_rate set net_rating = ? where location = ?;", bsns_tuple)
	
	db.commit()
	db.close()

# Only use on a business that you are sure is added 
def get_rate(bsns_place):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	place_tuple = (bsns_place, )
	c.execute("select net_rating from bsns_rate where location = ?;", place_tuple)
	response = c.fetchone()
	if (response != None):
		return int(response[0])
	else:
		return -0.5 #Something went wrong

	db.commit()
	db.close()

def add_hotel(name, coors, arprt):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	place_tuple = (coors, )
	c.execute ("select * from hotels where location = ?;", place_tuple)
	response = c.fetchone()
	if( response == None):
		hotel_tuple = (name, coors, arprt)
		c.execute("insert into hotels values (?, ?, ?);", hotel_tuple)

	db.commit()
	db.close()

def get_hotels(arprt):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	arprt_tuple = (arprt, )
	c.execute("select * from hotels where close_arprt = ?;", arprt_tuple)
	response = c.fetchall()
	return response

	db.commit()
	db.close()
"""
# Testing
setup()

def reg_test(usnam, psword):
	if (registrate(usnam, psword)):
		print("First registration for " + usnam)
	else:
		print("Repeat registration for " + usnam)

reg_test("Heebies", "welp")
reg_test("Cold Embers", "Sister Friede?")
reg_test("Heebies", "welp")
reg_test("Heebies", "welp")
if( not password_check("Cold Embers", "Sister Friede")):
	print("Good negative response")
else:
	print("Bad positive response")
if (password_check("Heebies", "welp")):
	print("Good positive response")
else: 
	print("Bad negative response")

add_bsns("Lucky Charms", "Somewhere Over the Rainbow")
add_bsns("Joe's Pizza", "Near Gabriel's House")

rate_bsns("Somewhere Over the Rainbow", 1)
rate_bsns("Somewhere Over the Rainbow", -1)
rate_bsns("Somewhere Over the Rainbow", -1)
"""