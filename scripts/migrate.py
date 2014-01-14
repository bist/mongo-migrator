#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os
import yaml
import cx_Oracle
import datetime
os.environ["NLS_LANG"] = "AMERICAN_AMERICA.UTF8"

def rows_as_dicts(cursor,configuration,index):
	""" returns cx_Oracle rows as dicts """
	colnames = []
	for i in cursor.description:
		if i[0] in configuration['tables'][index]['columns']:
			colnames.append(configuration['tables'][index]['columns'][i[0]])
	
	for row in cursor:
		yield dict(zip(colnames, row))

def readFromOracle(configuration,index):
	oracleConnection = cx_Oracle.connect(configuration['oracle_configuration']['username'] + "/" + 
													 configuration['oracle_configuration']['password'] + "@" + 
													 configuration['oracle_configuration']['ip'] + "/" + 
													 configuration['oracle_configuration']['instance'])
	oracleCursor = oracleConnection.cursor()
	oracleCursor.execute('select count(*) from ' + configuration['tables'][index]['table_name'])

	print "Number of records at Oracle :" 
	print oracleCursor.fetchall()

	oracleCursor.execute('select * from ' + configuration['tables'][index]['table_name'])
	return rows_as_dicts(oracleCursor,configuration,index)

def insertMongo(data,configuration,index):
	mongoClient = MongoClient(configuration['mongo_server']['ip'], configuration['mongo_server']['port'],w=1)
	db = mongoClient[configuration['mongo_server']['collection']]
	for i in data:
		db[configuration['tables'][index]['collectionName']].insert(i)
	print "Number of records migrated to Mongo :" 
	print db[configuration['tables'][index]['collectionName']].count()

def loadConfiguration():
	""" loads yml configuration file"""
	f = open('migration_config.yml')
	configuration = yaml.safe_load(f)
	f.close()
	return configuration

def main():
	configuration = loadConfiguration()
	for index in range(len(configuration['tables'])):
		print "Table to be migrated :" + configuration['tables'][index]['table_name']
		data   = readFromOracle(configuration,index)
		result = insertMongo(data,configuration,index)

if __name__ == "__main__":
	main()
