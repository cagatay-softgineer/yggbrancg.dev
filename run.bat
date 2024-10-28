echo python -m uvicorn app.main:app --port 8000
uvicorn app.main:app --host 0.0.0.0 --port 8080
pause