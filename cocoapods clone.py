from git import *
import datetime
from functions import element_add
from functions import file_loop as fl
import glob
import json
import pandas as pd
from sqlalchemy import create_engine

##Cloning from the github repository
Repo.clone_from('https://github.com/CocoaPods/Specs', './cocoapods_repo')
repo = Repo("./cocoapods_repo")
o = repo.remotes.origin
o.pull()

##Getting the latest commit for each clone
master = repo.head.reference
latest_commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)

##Getting all the json files
list_of_files = glob.glob('./cocoapods_repo/Specs/*')
json_master = fl(fl(fl(fl(fl(list_of_files)))))


##Parsing json into dataframe
id_raw = 0
library_id = 100
table_1_master = []
table_2_master = []

for k in json_master:
    if k.endswith("json"):
        table_1_array = []
        table_2_array = []
        table_1_array.append(library_id)
        table_2_array.append(id_raw)

        with open(k, encoding="utf8", errors='ignore') as json_file:
            data = json.load(json_file)

            element_add('name', table_1_array)

            if 'description' in data.keys():
                element_add('description', table_1_array)
            else:
                element_add('summary', table_1_array)

            element_add('version', table_2_array)

            element_add('license', table_2_array)

        table_2_array.append(library_id)
        table_1_master.append(table_1_array)
        table_2_master.append(table_2_array)

        id_raw += 1
        library_id += 1
library = pd.DataFrame(table_1_master, columns = ['ID', 'Name', 'Description'])
library_version = pd.DataFrame(table_2_master, columns = ['ID', 'Name', 'Description', 'Library_ID (Fk)'])

##Check for the latest new commits and add the commit date to the dataframe
raw_library_version = pd.read_sql_table('library_version', 'postgres:///db_name')
library_version_dictionary = {'library_version_1':raw_library_version,'library_version_2':library_version}
library_version_new = pd.concat(library_version_dictionary)
library_version_new = library_version_new.drop_duplicates(keep=False)
library_version_new['Release_Date'] = latest_commit_date

raw_library= pd.read_sql_table('library', 'postgres:///db_name')
library_dictionary = {'library_1':raw_library_version,'library_2':library_version}
library_new = pd.concat(library_dictionary)
library_new = library_new.drop_duplicates(keep=False)

##Creating an engine to update the tables in postgres for each of the new data
engine = create_engine('postgres:///db_name', echo=False)
library_new.to_sql('library', con=engine, if_exists='append')
library_version_new.to_sql('library_version', con=engine, if_exists='append')
