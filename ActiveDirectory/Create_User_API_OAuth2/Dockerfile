FROM python:3.12-slim

# Install dependencies
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt  # Assume you have a requirements.txt; create one with pip freeze if needed

# Expose port (adjust if your API uses a different port, e.g., 5000 for Flask)
EXPOSE 8000

# Run the app (adjust entry point, e.g., 'python app.py' or 'uvicorn main:app --host 0.0.0.0 --port 8000')
CMD ["python", "main.py"]
