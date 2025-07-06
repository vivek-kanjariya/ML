# Backend API Node.js

## How to run

1. Install dependencies:
   ```sh
   npm install
   ```
2. Start the server:
   ```sh
   npm start
   ```
   Or for development with auto-reload:
   ```sh
   npm run dev
   ```

## Endpoints
- `POST /api/predict` — sample endpoint (replace logic in `src/controllers/predictController.js`)
- `GET /healthz` — health check

## Project Structure
- `src/app.js` — main app entry
- `src/routes/` — route definitions
- `src/controllers/` — business logic
- `src/utils/logger.js` — logging setup
- `.env` — environment variables
- `logs/` — log files

## Next Steps
- Migrate your business logic from FastAPI to the controllers.
- Add more routes/controllers as needed.
- For ML, call Python microservices or REST APIs if needed.
