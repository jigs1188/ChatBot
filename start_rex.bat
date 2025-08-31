@echo off
echo 🦾 Starting Rex AI Assistant...
echo.

:: Activate virtual environment
call venv\Scripts\activate

:: Set environment variable
set OPENROUTER_API_KEY=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

:: Start the application
echo 🚀 Launching Rex AI at http://localhost:5000
echo Press Ctrl+C to stop
echo.
python main.py

pause
