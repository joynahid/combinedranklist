import re

def getSheetName(shared_sheet_link):
    sheet_name = re.findall(r'#gid=.+$', shared_sheet_link)
    sheet_name = int(sheet_name[0][5:])
    return sheet_name

def format_sheet(id):
    id = getSheetName(id)

    standings_format = {
        'requests': [
            {
                'repeatCell': {
                    'range': {
                        "sheetId": id,
                        "startRowIndex": 0,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'horizontalAlignment': 'CENTER',
                            'textFormat': {
                                'fontFamily': 'Roboto Mono'
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(horizontalAlignment, textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': {
                        "sheetId": id,
                        "startRowIndex": 0,
                        "startColumnIndex": 2,
                        "endColumnIndex": 5
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {
                                'bold': True,
                                'fontFamily': 'Roboto Mono'
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(textFormat)'
                }
            },
            {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': id,
                        'gridProperties': {
                            'frozenRowCount': 2,
                        }
                    },
                    "fields": "gridProperties(frozenRowCount, frozenColumnCount)"
                }
            }
        ]
    }

    return standings_format
