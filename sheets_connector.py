# sheets_connector.py

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def write_to_sheet(data: dict, spreadsheet_id: str, creds_json: dict) -> bool:
    try:
        creds = Credentials.from_service_account_info(creds_json, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id).sheet1

        # Подготовка строки
        row = [
            data.get("Дата", datetime.now().strftime("%Y-%m-%d")),
            data.get("Время", datetime.now().strftime("%H:%M")),
            data.get("Прием пищи", ""),
            data.get("Ккал", ""),
            data.get("Белки (г)", ""),
            data.get("Жиры (г)", ""),
            data.get("Углеводы (г)", "")
        ]

        sheet.append_row(row)
        return True

    except Exception as e:
        print(f"Ошибка записи в Google Sheets: {e}")
        return False
