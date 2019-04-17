# The task for this week is following: I am attaching forex.db which is a sqlite3 DB.
#
# You need to write a script that would check the data within the forex.sqlite3 (this is sqlite3 DB attached)
# and compare it against the data fetched at run-time from https://api.exchangeratesapi.io/latest
# Inside the DB, there is a table created with CREATE TABLE rates (currency_code text, currency_name text, rate real)
# In case if the exchange rate is different, update the rate column with the new value.
# In case if the API has no value for a currency present in the DB, delete the corresponding DB row.
# If API has a currency that does not exist in the DB, add a new row to the DB;
# leave the currency_name column for the new currencies empty.

# Bonus points for the following: during script execution, create a CSV report with the following contents:
# currency_code, old_rate, new_rate, percent_change
# USD, 1.1321, 1.15, +1.58%
# …



##########################################################
#suggested improvements:
#separate logging into a sepaarte function
#iterate over deletions also, and use parametrized query
#get all configs into a external json file
##########################################################

import sqlite3
import requests
import json
import csv

EXC_SERVICE_URL = 'https://api.exchangeratesapi.io/latest'
LOG_FILE = 'log.csv'
DB_FILE = 'forex.sqlite3'

#get dict of rates to 1 EUR
def get_rates_dict(exchange_url):
     response = requests.get(EXC_SERVICE_URL).text
     return json.loads(response)['rates']

#get string of existing currencies from rates_dict for sql query
def get_currencies(rates_dict):
    return '\'' + '\',\''.join(rates_dict) + '\''

#calculate percentage change in a nice format
def get_percentage_change(old_rate, new_rate):
    result = round( (new_rate/old_rate - 1) * 100, 2 )
    if result > 0:
        return '+{}%'.format(result)
    else:
        return '{}%'.format(result)

#update / insert new records, and log results into csv file
def update_insert_db(db_file, rates_dict):
    #open connection to DB
    with sqlite3.connect(db_file) as connection:
        #ToDO - doesn't work with ? and parametrized query... need to debug
        sql_parameterized_query = 'SELECT rate FROM rates WHERE currency_code = \'{}\''
        cursor = connection.cursor()
        #open log file to log actions
        with open(LOG_FILE, mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')

            #for each currency do this
            for record in rates_dict:
                #run query and check if the record exists in DB
                cursor.execute(sql_parameterized_query.format(record))
                db_record = cursor.fetchall()

                if len(db_record) == 0:
                    #currency doesnot exist instering
                    insert_query = 'INSERT INTO rates VALUES (?, ?, ?)'
                    cursor.execute(insert_query,(record,None,rates_dict[record]))
                    writer.writerow([record,'',rates_dict[record],'n/a'])
                else:
                    #currency exists need to update
                    update_query = 'UPDATE rates SET rate = ? WHERE currency_code = ?'
                    cursor.execute(update_query,(rates_dict[record],record))
                    writer.writerow([record,
                                     list(db_record[0])[0],
                                     rates_dict[record],
                                     get_percentage_change(list(db_record[0])[0],
                                                           float(rates_dict[record]))])


#delete obsolete records, no logging as they do not exist anymore
def delete_db(db_file, rates_dict):
    with sqlite3.connect(db_file) as connection:
        sql_parameterized_query = 'DELETE FROM rates WHERE currency_code NOT IN ({})'
        cursor = connection.cursor()
        #format as a hack to remove number of records,
        # parametrized query has to get a number of items in IN clause
        cursor.execute(sql_parameterized_query.format(get_currencies(rates_dict)))


####################################################################
#################### let's roll#####################################
####################################################################
if __name__ == "__main__":
    rates_dict = get_rates_dict(EXC_SERVICE_URL)
    curr = get_currencies(rates_dict)

    update_insert_db(DB_FILE, rates_dict)
    delete_db(DB_FILE, rates_dict)