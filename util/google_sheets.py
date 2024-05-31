#Required for Google Sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime

def add(sheet_id, email_subject, email_date, email_sender, deadline, email_summary, file_link):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('tokens/credentials_sheets.json', scope)
    gc = gspread.authorize(credentials)
    sheet_id = sheet_id  
    sheet = gc.open_by_key(sheet_id).sheet1
    next_row = len(sheet.get_all_values()) + 1
    now = datetime.now()
    current_datetime = now.strftime('%d/%m/%Y %H:%M:%S')
    sheet.update_cell(next_row, 1, current_datetime)
    sheet.update_cell(next_row, 2, email_date)
    sheet.update_cell(next_row, 3, deadline)
    sheet.update_cell(next_row, 4, email_sender)
    sheet.update_cell(next_row, 5, email_subject)
    sheet.update_cell(next_row, 6, email_summary)
    sheet.update_cell(next_row, 7, file_link)