# Feather Backend (Flask) — Sprint 1 (FEA-40)

## Quick Start

```bash
# 1️. Create a virtual environment
python -m venv .venv

# 2️. Activate it
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# 3. Install required frameworks
pip install -r requirements.txt

# 4. Copy environment file
# Windows
copy .env.example .env
# macOS/Linux
cp .env.example .env

# 5️. Run the backend
python wsgi.py
# Server will start at: http://127.0.0.1:5000/health

Basic File Structure:

app folder -- Contains main Backend code
app/__init__.py -- Creates and configures the Flask app
app/config.py -- Loads Environment variables and settings
app/extensions.py -- Initializes global utilities( CORS, repo, etc.)

api folder -- contains the route blueprints

services folder -- contains helper logic or mini modules(non-api logic)

wsgi.py -- Creates the app and runs it

app/__init__.py -- Builds the flask app, loads the settings, enables CORS and registers the API routes.

    - config.py --> loads env
    - extensions.py --> initializes CORS and repository
    - api/__init__.py --> connects your endpoints(routes)