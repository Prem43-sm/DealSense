@echo off
setlocal

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
  echo Creating Python virtual environment...
  python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing backend requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Running Alembic migrations...
python -m alembic upgrade head

echo Starting DealSense FastAPI backend...
uvicorn app.main:app --reload
