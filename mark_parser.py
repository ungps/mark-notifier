import os.path
import numpy
import math
import types
import time
import sys
import editdistance
import unidecode
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = 'REPLACE WITH SPREADSHEET ID'

PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

SHEET_NAME = 'REPLACE WITH SHEET_NAME'
RANGE_NAME = 'A1:AA1000'
GRADEBOOK = 'gradebook.csv'
GRADEBOOK_TMP = 'gradebook_tmp.csv'
CREDENTIALS = 'service-account.json'

STUDENT_NAME = "REPLACE WITH STUDENT NAME"

service = None

def findNameRow(df, name):
    searchName = name.lower().replace('-', '')
    minDist = sys.maxsize
    row = -1
    r, c = df.shape

    f = set()
    for i in range(r):
        for j in range(c):
            value = df.iat[i, j]

            if value == None:
                continue

            if not isinstance(value, str):
                continue

            valueLower = unidecode.unidecode(value).lower()
            dist = editdistance.eval(name.lower(), valueLower)
            if (dist < minDist):
                minDist = dist;
                row = i

    return row

def beautifyString(s):
    return unidecode.unidecode(s).replace('\n', ' ')

def login():
    global service
    creds = None

    credentials = service_account.Credentials.from_service_account_file(
        PATH + CREDENTIALS, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

def getDfDiff(oldDf, newDf, name):
    r2, c2 = newDf.shape

    oldR = findNameRow(oldDf, name)
    newR = findNameRow(newDf, name)

    diff = {}
    for i in range(c2):
        if oldDf.iat[oldR, i] == newDf.iat[newR, i]:
            continue

        if (isinstance(oldDf.iat[oldR, i], numpy.float64) or \
            isinstance(oldDf.iat[oldR, i], float)) and \
            (isinstance(newDf.iat[newR, i], numpy.float64) or \
            isinstance(newDf.iat[newR, i], float)) and \
            math.isnan(oldDf.iat[oldR, i]) and \
            math.isnan(newDf.iat[newR, i]):
            continue

        diff[beautifyString(newDf.columns.values[i])] = [oldDf.iat[oldR, i], newDf.iat[newR, i]]

    return diff

def getValues():
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SHEET_NAME + "!" + RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

    return values_input

def getValuesDf():
    values = getValues()
    return pd.DataFrame(values[1:], columns=values[0])

def get_diff():
    login()

    if not os.path.isfile(PATH + GRADEBOOK):
        newDf = getValuesDf()
        newDf.to_csv(PATH + GRADEBOOK)
        return {}

    oldDf = pd.read_csv(PATH + GRADEBOOK, header = 0, index_col = 0)

    # Get same format
    newDf = getValuesDf()
    newDf.to_csv(PATH + GRADEBOOK_TMP)
    newDf = pd.read_csv(PATH + GRADEBOOK_TMP, header = 0, index_col = 0)

    diff = getDfDiff(oldDf, newDf, STUDENT_NAME)
    newDf.to_csv(PATH + GRADEBOOK)
    return diff
