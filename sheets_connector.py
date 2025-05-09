# sheets_connector.py

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _connect(creds_json: dict, spreadsheet_id: str):
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    return sheet

def write_meal(creds_json, spreadsheet_id, date: str, meal_type: str, description: str, kcal_data: dict):
    sheet = _connect(creds_json, spreadsheet_id)
    worksheet = sheet.worksheet("Питание")

    row = [
        date,
        meal_type,
        description,
        kcal_data.get("Ккал", ""),
        kcal_data.get("Белки (г)", ""),
        kcal_data.get("Жиры (г)", ""),
        kcal_data.get("Углеводы (г)", "")
    ]

    worksheet.append_row(row)

def write_hydration(creds_json, spreadsheet_id, water_ml: int, caffeine_ml: int):
    sheet = _connect(creds_json, spreadsheet_id)
    worksheet = sheet.worksheet("Гидратация")

    total = water_ml - caffeine_ml

    row = [
        datetime.now().strftime("%Y-%m-%d"),
        water_ml,
        caffeine_ml,
        total
    ]

    worksheet.append_row(row)

def write_vitamins(creds_json, spreadsheet_id, description: str):
    sheet = _connect(creds_json, spreadsheet_id)
    worksheet = sheet.worksheet("Витамины")

    row = [
        datetime.now().strftime("%Y-%m-%d"),
        description
    ]

    worksheet.append_row(row)

def write_workout(creds_json, spreadsheet_id, workout_dict: dict):
    sheet = _connect(creds_json, spreadsheet_id)
    worksheet = sheet.worksheet("Нагрузка")

    row = [datetime.now().strftime("%Y-%m-%d")]

    # Упорядоченный список активностей (по колонкам)
    activity_order = ["разминка", "бег интенсивный", "бег лёгкий", "силовая", "йога", "велосипед", "плавание", "хайкинг", "ходьба"]

    for activity in activity_order:
        row.append(workout_dict.get(activity, ""))

    worksheet.append_row(row)
