# Fanbase Builder Frontend

React frontend for the Fanbase Builder music marketing platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173` and proxy API requests to `http://localhost:8000`.

## Environment Variables

Create a `.env` file in the frontend directory:

```
VITE_API_URL=http://localhost:8000
```

## Features

- User authentication (login/signup)
- Onboarding interview (9 questions, one at a time)
- Protected routes
- Dashboard (basic)

## Tech Stack

- React 18
- React Router 6
- Vite
- Axios

