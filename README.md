# Smart Parking System

Flask + SQLite backend with MVC (models, controllers, views) and a React + Vite frontend. SMS lookup via Twilio webhook.

## Prerequisites
- Python 3.11.9
- Node 18+

## Environment Configuration

Create environment files for backend and frontend.

Backend (create `backend/.env`):

```
SECRET_KEY=dev-secret-key
# DATABASE_URL=sqlite:///absolute/or/relative/path.db
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
```

Frontend (create `frontend/.env`):

```
VITE_API_BASE_URL=http://localhost:5000
```

## Install & Run

Backend:

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# load env
Set-Location ..
python -m backend.app
```

Frontend:

```powershell
cd frontend
npm install
npm run dev -- --port 3000
```

## API Overview

- POST `/api/tickets` – create ticket
- GET `/api/tickets` – list (supports `isActive`, `licensePlate`, `ticketNumber`)
- GET `/api/tickets/<id>` – details
- PATCH `/api/tickets/<id>` – update
- POST `/api/tickets/<id>/checkout` – checkout
- GET `/api/tickets/search?q=...` – search by ticket/plate/spot
- POST `/sms` – Twilio webhook (x-www-form-urlencoded)

## Twilio Webhook

Expose your backend publicly (e.g. with ngrok) and set your Twilio number's Messaging webhook to:

```
POST https://<your-public-host>/sms
```

Send a license plate or ticket number to receive the parking spot in the reply.


