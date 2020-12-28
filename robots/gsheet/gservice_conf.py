import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT = {
  "type": os.environ.get('SHEET_TYPE'),
  "project_id": os.environ.get('PROJECT_ID'),
  "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
  "private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n'),
  "client_email": os.environ.get('CLIENT_EMAIL'),
  "client_id": os.environ.get('CLIENT_ID'),
  "auth_uri": os.environ.get('AUTH_URI'),
  "token_uri": os.environ.get('TOKEN_URI'),
  "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER'),
  "client_x509_cert_url": os.environ.get('CLIENT_URL')
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT, scopes= SCOPES)

drive_service = build('drive','v3', credentials=creds)
sheet_service = build('sheets', 'v4', credentials=creds)