# gspread library:
# •	https://gspread.readthedocs.io/en/latest/index.html
# •	Credential setup https://gspread.readthedocs.io/en/latest/oauth2.html

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('config_gs.json', scope)
gc = gspread.authorize(credentials)

wks = sht1 = gc.open_by_key('...').sheet1
