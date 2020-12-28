import re
from robots.gsheet.gservice_conf import drive_service, sheet_service

def getSheetId(shared_sheet_link):
    sheet_id = re.findall(r'/d/.+/', shared_sheet_link)
    ln = len(sheet_id)
    if ln!=1: return shared_sheet_link
    sheet_id = sheet_id[0][3:-1]
    return sheet_id

def retrieve(sheet_link, sheet_range, dimension):
    sheet_id = getSheetId(sheet_link)
    result = sheet_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_range, majorDimension = dimension).execute()
    values = result.get('values')
    return values

def create_sheet(title):
    if not title:
        return 'NoTitleFound'

    title+= ' (by RAPL Robot)'

    spreadsheet = {
        'properties': {
            'title': title
        }
    }

    spreadsheet = sheet_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()

    file_id = spreadsheet.get('spreadsheetId')

    return file_id

def change_owner(owner_email, file_id):
    user_permission = {
        'type': 'user',
        'role': 'owner',
        'emailAddress': owner_email
    }
    
    req = drive_service.permissions().create(fileId=file_id, body=user_permission, fields="id")
    response = req.execute()

    print(response)

def update(from_,  data, link = None, _formatting= None):
    spreadsheet_id = getSheetId(link)
    range_ = from_

    value_input_option = 'USER_ENTERED'

    value_range_body = {
        'values': data
    }

    if _formatting:
        req = sheet_service.spreadsheets().batchUpdate(spreadsheetId = spreadsheet_id, body = _formatting).execute()
    
    clr = sheet_service.spreadsheets().values().clear(spreadsheetId = spreadsheet_id, range = "Sheet1!A1:AA1000", body = {}).execute()

    request = sheet_service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()

# main('1mtshftAafZ7VkVqtAk__CVZBJQlZmXAxF8Z9M8EXWcg')