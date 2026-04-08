# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables preventing python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
# PORT will be overridden by Render at runtime (defaults to 10000)
ENV PORT=10000

# Set the working directory
WORKDIR /app

# Install system utilities needed by RDKit and LightGBM
# libgomp1 is required by LightGBM
# libxrender1, libxext6 are required by RDKit C++ bindings
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY backend/requirements.txt ./backend/

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Copy the entire backend and frontend directories
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose the port (Render will map this automatically)
EXPOSE 10000

# Move into backend directory where app.py lives
WORKDIR /app/backend

# Run the waitress production server
CMD ["python", "app.py"]
