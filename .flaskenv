# === Environment variables that will be automatically loaded when launching the server ===
# Only work in development (gunicorn required for production)

# Enable debug mode
FLASK_DEBUG=1
# Environement
FLASK_ENV=development
# Port used for the server
FLASK_RUN_PORT=5000

# Main file (don't change)
FLASK_APP=flask_engine.py