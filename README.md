# Telegram-бот для любимой ❤️

Telegram-бот для девушки на время отсутствия заказчика в армии.

## Функции

- ⏰ Таймер обратного отсчёта с прогресс-баром
- 😊 Дневник настроения с графиками
- 📝 Личный дневник для записей
- ✉️ Весточки для заказчика
- 💌 Случайные тёплые фразы
- 📸 Случайные фото
- 🌅 Ежедневная автоматическая рассылка

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd бот дем
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте `.env` файл:
```
BOT_TOKEN=ваш_токен_от_BotFather
OWNER_USERNAME=ваш_username
DEPARTURE_DATE=2026-06-28 22:00
RETURN_DATE=2026-08-02
DAILY_SCHEDULE_1=09:00
DAILY_SCHEDULE_2=20:00
```

4. Запустите бота:
```bash
python bot.py
```

## Добавление фото

Добавьте фото в папку `data/photos/`. Бот будет отправлять случайные фото из этой папки.

## Команды для заказчика

- `/diary_all` — просмотреть все записи дневника
- `/secret_all` — просмотреть все весточки
- `/export` — экспортировать все данные в файл

## Развёртывание на облачном хостинге

### Render.com

1. Создайте новый репозиторий на GitHub и загрузите код
2. Зайдите на [render.com](https://render.com) и создайте новый Web Service
3. Выберите Python
4. Подключите репозиторий
5. В настройках добавьте переменные окружения из `.env`
6. В Build Command укажите: `pip install -r requirements.txt`
7. В Start Command укажите: `python bot.py`

### PythonAnywhere

1. Загрузите файлы на PythonAnywhere
2. Создайте virtual environment:
```bash
mkvirtualenv bot
pip install -r requirements.txt
```
3. Добавьте переменные окружения в `.bashrc`
4. Создайте Bash script для запуска бота
5. Настройте always-on task

## Структура проекта

```
бот дем/
├── bot.py                    # Главный файл бота
├── config.py                 # Конфигурация
├── database.py               # Работа с БД
├── handlers/                 # Хендлеры
│   ├── start.py
│   ├── countdown.py
│   ├── mood.py
│   ├── diary.py
│   ├── secret.py
│   ├── content.py
│   └── owner.py
├── keyboards/                # Клавиатуры
│   └── inline.py
├── utils/                    # Утилиты
│   ├── timer.py
│   └── charts.py
├── data/                     # Данные
│   └── photos/
├── .env                      # Токен и конфиг
├── requirements.txt          # Зависимости
└── README.md                 # Инструкция
```

## Технологии

- Python 3.10+
- aiogram 3.x
- SQLite
- matplotlib
- python-dotenv
