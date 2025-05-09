## 📄 `README.md`

````markdown
# Helpik – Telegram-бот для трекинга еды, КБЖУ и записи в Google Sheets

**Helpik** — это персональный бот в Telegram, который помогает отслеживать:
- приёмы пищи
- КБЖУ по базе продуктов
- и записывать всё в Google Таблицу для анализа

---

## 🚀 Быстрый старт

### 1. Создайте `.env` на основе примера

Скопируйте `.env.example` → `.env` и заполните:

```env
TELEGRAM_TOKEN=токен от BotFather
SPREADSHEET_ID=ID Google-таблицы
GOOGLE_CREDS_JSON={"type": "service_account", "...": "..."}  # В одну строку
````

---

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

---

### 3. Запустите бота

```bash
python bot.py
```

Бот начнёт слушать сообщения и записывать в таблицу приёмы пищи с КБЖУ.

---

## 🧾 Пример использования

В Telegram напишите:

```
завтрак: овсянка 60г, банан 100г, мёд 1 ч.л.
```

Бот распознает продукты, рассчитает:

* калории
* белки
* жиры
* углеводы

И отправит строку в Google Sheets.

---

## ☁️ Деплой на Render.com

1. Зарегистрируйтесь на [https://render.com](https://render.com)

2. Создайте Web Service

3. Подключите репозиторий

4. Укажите:

   * **Build Command:**

     ```bash
     pip install -r requirements.txt
     ```

   * **Start Command:**

     ```bash
     python bot.py
     ```

5. Установите переменные окружения:

   * `TELEGRAM_TOKEN`
   * `SPREADSHEET_ID`
   * `GOOGLE_CREDS_JSON` (одна строка)

6. Бот заработает по Webhook

---

## 📎 Примечания

* Все КБЖУ берутся из базового словаря `PRODUCT_DB` в `kcal_parser.py`
* В будущем можно подключить внешний API для расчёта
* Не храни `GOOGLE_CREDS.json` в репозитории!

