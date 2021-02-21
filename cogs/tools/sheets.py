import httplib2
import os
import configparser

from apiclient import discovery


def get_pf_sheet():
    auth = open(os.getcwd() + "/auth.ini")
    cfgParser = configparser.ConfigParser()
    cfgParser.read_file(auth)
    key = cfgParser.get("google", "key")

    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build(
        'sheets',
        'v4',
        http=httplib2.Http(),
        discoveryServiceUrl=discoveryUrl,
        developerKey=key)

    spreadsheetId = '1cqjnKrvx2qjqlI09K8HapGoBxq42wOsFn87_t8xxn5s'

    # legend = service.spreadsheets().values().get(
    #     spreadsheetId=spreadsheetId, range='A1:CD1'
    # ).execute().get('values', [])
    #
    # result = service.spreadsheets().values().get(
    #     spreadsheetId=spreadsheetId, range='A2:E').execute()
    # values = result.get('values', [])

    return service.spreadsheets().values()
