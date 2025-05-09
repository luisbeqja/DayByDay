# Vue PWA with Flask Backend Boilerplate

A clean boilerplate for building Progressive Web Apps (PWA) with Vue 3, TypeScript, and Python Flask backend.

## Features

- Vue 3 Composition API with TypeScript
- Pinia for state management
- RESTful API with Flask
- PWA capabilities including offline support
- Push notification support
- Responsive design

## Project Structure

```
.
├── frontend/          # Vue.js frontend application
│   ├── public/        # Static assets
│   │   └── sw.js      # Service Worker for push notifications
│   └── src/           # Source code
│       ├── assets/    # Images, fonts, etc.
│       ├── components/# Vue components
│       ├── router/    # Vue Router configuration
│       ├── services/  # Services including notification handling
│       ├── stores/    # Pinia stores
│       └── views/     # Vue views/pages
└── backend/           # Flask backend application
    ├── app.py         # Main Flask application
    ├── requirements.txt # Python dependencies
    └── venv/          # Python virtual environment
```

## Setup and Running

### Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build
```

### Backend

```bash
# Navigate to backend directory
cd backend

# Set up virtual environment (if not already done)
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

## API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/info` - Get application information
- `GET /api/vapid-public-key` - Get the VAPID public key for push subscriptions
- `POST /api/notifications/subscribe` - Register a push subscription
- `POST /api/notifications/unsubscribe` - Remove a push subscription
- `POST /api/notifications/send` - Send a push notification to all subscribers

## Push Notifications

This boilerplate includes a complete push notification system using the Web Push API:

1. **Service Worker**: Handles background push events even when the app is closed
2. **Notification Service**: TypeScript service to manage notification permissions and subscriptions
3. **Backend Integration**: Flask endpoints to manage subscriptions and send push notifications

### VAPID Keys Setup

For push notifications to work, you need to generate VAPID keys:

```bash
# Install the web-push CLI
npm install -g web-push

# Generate VAPID keys
web-push generate-vapid-keys

# Add the keys to your backend/.env file
echo "VAPID_PUBLIC_KEY=your_public_key" >> backend/.env
echo "VAPID_PRIVATE_KEY=your_private_key" >> backend/.env
```

## Development

This project uses ESLint and Prettier for code formatting. To format your code:

```bash
# In the frontend directory
npm run format
```

## Adding New Features

### Frontend

1. Create new components in `frontend/src/components/`
2. Add routes in `frontend/src/router/index.ts`
3. Create stores with Pinia in `frontend/src/stores/`

### Backend

1. Add new API endpoints in `backend/app.py`
2. Install additional Python packages as needed and update `requirements.txt` 