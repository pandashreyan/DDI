# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables preventing python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PORT=5005

# Set the working directory
WORKDIR /app

# Install system utilities needed by RDKit or LightGBM if necessary. 
# libgomp1 is usually required by LightGBM
# libxrender1, libxext6 are requested by RDKit C++ bindings
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY backend/requirements.txt ./backend/

# Install python dependencies natively
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Copy the entire backend and frontend directories
# Since frontend is served statically by the flask app using path relative to backend we need both
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose the API port
EXPOSE 5005

# Move into backend directory where app.py lives
WORKDIR /app/backend

# Run the waitress production server wrapper (as defined inside app.py)
CMD ["python", "app.py"]
