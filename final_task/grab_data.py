import requests
import json
import calendar
import pyodbc

#constants and default params
YEAR = 2017
DB = 'olx'
SERVER = 'localhost'
BASE_URL = 'https://35.204.204.210/{}-{}-{}/'
EMPTY_RESPONSE = '{\'postings\': []}'
BASE_INSERT = 'INSERT INTO [olx].[dbo].[Apartment] ' \
              '(price_usd,title,text,total_area,kitchen_area,living_area,location,number_of_rooms,added_on) ' \
              'VALUES (?,?,?,?,?,?,?,?,?)'
FIELDS = [
    'price_usd', 'title', 'text', 'total_area', 'kitchen_area', 'living_area',
    'location', 'number_of_rooms', 'added_on'
]


#format day or month with to match 2-digit format
def format_two_digits(str):
    length = len(str)
    if length == 2:
        return str
    elif length == 1:
        return '0' + str
    else:
        raise Exception(
            'str should be a month or day number of length 2, and it\'s {}'
            .format(str))


#get URLs for a given year
def get_urls_by_year(year):
    url_list = []
    months = list(range(1, 13))
    for month in months:
        num_days = calendar.monthrange(year, month)[1]
        days = list(range(1, num_days + 1))
        for day in days:
            url_list.append(
                BASE_URL.format(year, format_two_digits(str(month)),
                                format_two_digits(str(day))))
    return url_list


#get data from rest API (OLX postings)
def get_data_by_url(url):
    #verify false, becaue OLX uses self-sgned certificate
    response = requests.get(url, verify=False)
    return json.loads(response.text)


#validate if is empty - no records this day
def validate_response(response):
    if str(response) == EMPTY_RESPONSE:
        return False
    else:
        return True


#get connection to ms sql server
def get_sqls_conn(server, db):
    conn = pyodbc.connect('Driver={SQL Server};' #SQL Server 2014
                          'Server=' + server + ';'
                          'Database=' + db + ';'
                          'Trusted_Connection=yes;')#trusted connection auth
    return conn


#insert a row into sql server
def insert_row_in_sqls(connection, data):
    connection.cursor().execute(
        BASE_INSERT,
        (data['price_usd'], data['title'], data['text'], data['total_area'],
         data['kitchen_area'], data['living_area'], data['location'],
         data['number_of_rooms'],
         data['added_on'].split('T')[0]))  #getdate only
    connection.commit()


#populate DB woth records from rest API
def populate_DB_from_OLX_REST():
    urls = get_urls_by_year(YEAR)
    conn = get_sqls_conn(SERVER, DB)

    for url in urls:
        data = get_data_by_url(url)
        print('URL: ' + url)
        if validate_response(data):
            print('Active records: ' + str(len(data['postings'])))
            for record in data['postings']:
                insert_row_in_sqls(conn, record)
        else:
            print('No active records')
    conn.close()


#########let's do the work - grab data from OLX and save to SQL Server###########
if __name__ == '__main__':
    populate_DB_from_OLX_REST()
