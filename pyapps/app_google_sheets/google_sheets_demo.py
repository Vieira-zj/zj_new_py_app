# coding: utf-8

import pickle
import os.path
import pandas as pd

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_creds():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def quick_start():
    '''
    https://developers.google.com/sheets/api/quickstart/python
    '''

    sheet_id = '1_kOrMEEYH-R09NWE2dHO_JloHgfLAr5THhuDI4q-pmU'
    range_name = 'User-center接口!A:B'

    service = build('sheets', 'v4', credentials=get_creds())

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values[:10]:
            # Print columns A and B
            print('%s, %s' % (row[0], row[1]))


def google_sheets_with_pd():
    sheet_id = '1_kOrMEEYH-R09NWE2dHO_JloHgfLAr5THhuDI4q-pmU'
    range_name = 'User-center接口!A:F'

    service = build('sheets', 'v4', credentials=get_creds())
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    if len(values) == 0:
        return

    cols = values[0]
    rows = values[1:]
    df = pd.DataFrame(rows, columns=cols)
    print('total cases:', len(df))

    done = df.loc[lambda x: x['Status'] == 'done']
    print('done cases:', len(done))
    print(done[:10])


if __name__ == '__main__':

    # quick_start()
    google_sheets_with_pd()
    print('google sheets done')
