mongo-migrator
==============

This script can be used to migrate from Oracle to Mongo. migrate.py 
script uses migration_config.yml file to hold configurations. You
can edit migration_config.yml file to fit your needs. 

There are three sections in migration_config.yml file. First section
is used for Oracle database server's connection information. This
sections begins with oracle_configuration element:

	change username_of_db field according to your Oracle's db user
	change password_of_db_user field to your Oracle password
	change ip_address_for_db field to your Oracle's IP address
	change instance_name_for_db field to your Oracle's instance name

Second section of configuration file contains information about Mongo 
server. This section starts with mongo_server element:

	change ip_address_for_mongo field to your MongoDB's IP address
	change port if MongoDB is running on another port
	change collection_name_for_mongo to your MongoDB collection name

Third section of configuration file contains information about tables 
which would be migrated. This section starts with tables element. This
element can hold multiple data:

	change table_name field to your Oracle table name
	change collectionName to your MongoDB collection name
	columns array can contain table field and mongo field matching.

