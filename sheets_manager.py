import gspread
from google.oauth2.service_account import Credentials

class SheetsManager:
    def __init__(self, credentials_file, spreadsheet_name, worksheet_name="Datos"):
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.worksheet_name = worksheet_name
        self.gc = None
        self.worksheet = None

    def setup_google_sheets(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_file(
            self.credentials_file, scopes=scope
        )
        self.gc = gspread.authorize(credentials)
        spreadsheet = self.gc.open(self.spreadsheet_name)
        try:
            self.worksheet = spreadsheet.worksheet(self.worksheet_name)
        except gspread.WorksheetNotFound:
            self.worksheet = spreadsheet.add_worksheet(
                title=self.worksheet_name, rows="1000", cols="20"
            )
        return self.worksheet

    def send_to_sheets(self, data):
        if not data:
            print("No hay datos para enviar")
            return
        headers = list(data[0].keys())
        try:
            existing_headers = self.worksheet.row_values(1)
            if not existing_headers:
                self.worksheet.append_row(headers)
        except:
            self.worksheet.append_row(headers)
        rows = []
        for item in data:
            row = [item.get(header, '') for header in headers]
            rows.append(row)
        if rows:
            self.worksheet.append_rows(rows)
            print(f"Se enviaron {len(rows)} filas a Google Sheets")
