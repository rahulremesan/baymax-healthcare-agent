# Baymax Healthcare Agent

Baymax is a self-hosted personal healthcare and accountability assistant that helps users build healthy habits through tracking, reminders, reports, and Telegram-based interactions.

Inspired by Baymax from Big Hero 6, this project focuses on daily discipline and health accountability.

---

## Features

### Health Tracking

Track:

* Water Intake
* Exercise
* Daily Steps
* Sleep Goals
* Wake-up Goals
* Breakfast Completion
* Learning Activities
* Alcohol Consumption

### Health Score Engine

Baymax calculates a daily score out of 100 based on goal completion.

| Activity               | Points |
| ---------------------- | ------ |
| Wake up before 6:30 AM | 15     |
| Water Goal (3L)        | 15     |
| Exercise               | 20     |
| Steps Goal (8000)      | 15     |
| No Alcohol             | 10     |
| Breakfast              | 10     |
| Learning               | 5      |
| Sleep Before 11 PM     | 10     |

Maximum Score: 100

### Telegram Bot

Interact directly from Telegram:

* Log water intake
* Update step count
* Mark exercise completion
* View score
* View daily report

### Reminder Engine

Baymax automatically sends:

* Morning reminders
* Water reminders
* Exercise reminders
* Sleep reminders

---

## Architecture

```text
Telegram
    ↓
Baymax Telegram Bot
    ↓
FastAPI
    ↓
SQLite
    ↓
Health Tracking Engine
    ↓
Scheduler
```

---

## Project Structure

```text
baymax-healthcare-agent/

├── app/
│   ├── config.py
│   ├── database.py
│   ├── health_service.py
│   ├── main.py
│   ├── models.py
│   ├── scheduler.py
│   ├── schemas.py
│   ├── telegram_bot.py
│   └── telegram_sender.py
│
├── data/
├── tests/
├── run_bot.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/rahulremesan/baymax-healthcare-agent.git

cd baymax-healthcare-agent
```

### Create Virtual Environment

```bash
python3 -m venv venv
```

Activate:

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```powershell
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Telegram Bot Setup

### Create Telegram Bot

1. Open Telegram
2. Search for `@BotFather`
3. Run:

```text
/newbot
```

4. Save the generated Bot Token

### Get Chat ID

Send a message to your bot.

Open:

```text
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

Locate:

```json
"chat": {
  "id": 123456789
}
```

Copy the ID.

---

## Environment Variables

Create a file named:

```text
.env
```

Add:

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
```

---

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Start Telegram Bot

Open a second terminal:

```bash
source venv/bin/activate

python run_bot.py
```

Expected:

```text
🤖 Baymax Telegram Bot Started
```

---

## Scheduler

Baymax uses APScheduler to send automatic reminders.

| Time     | Reminder          |
| -------- | ----------------- |
| 06:30 AM | Morning Goals     |
| 11:00 AM | Water Reminder    |
| 07:00 PM | Exercise Reminder |
| 10:00 PM | Sleep Reminder    |

---

## Telegram Commands

### Start

```text
/start
```

### Add Water

```text
/water 500
```

### Update Steps

```text
/steps 8500
```

### Exercise Completed

```text
/exercise
```

### View Score

```text
/score
```

### Daily Report

```text
/report
```

---

## API Endpoints

### Health Check

```http
GET /
```

### Today's Log

```http
GET /today
```

### Daily Report

```http
GET /report
```

### Health Score

```http
GET /health-score
```

### Create / Update Daily Log

```http
POST /daily-log
```

Example:

```json
{
  "water_ml": 3000,
  "exercise_done": true,
  "steps": 9000,
  "breakfast_done": true,
  "sleep_before_11": true,
  "wakeup_before_630": true,
  "learning_done": true
}
```

---

## Roadmap

### Version 1

* FastAPI Backend
* SQLite Storage
* Telegram Commands
* Daily Reports
* Scheduler Notifications

### Version 2

* Weight Tracking
* Weekly Reports
* Streak Tracking
* Progress Dashboard

### Version 3

* Google Fit Integration
* Sleep Tracking
* Step Synchronization

### Version 4

* AI Health Coach
* Personalized Recommendations
* Voice-Based Interaction

---

## License

MIT License

---

## Author

Rahul R

Baymax was built to provide a personal healthcare accountability system that helps transform health goals into consistent daily actions.

