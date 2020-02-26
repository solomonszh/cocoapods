# cocoapods

The cocoapods.py clone the cocoapods repository directly to your localhost. 

The project is then searched for the Specs json repositories and parsing of each json file for the necessary key, value will upadte the master list of lists of records. 

The list of lists of record for Library and Library Version will be converted to a dataframes each.

Existing database from postgres sql can be queried to dataframe to compare for new commit records. Afterwhich, these new commit records will update to the database after creating a postgres sql engine to append to existing database. 
