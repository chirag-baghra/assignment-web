FROM python:3.11-slim

# Set environment variables
ENV ACCEPT_EULA=Y
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    perl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft package repository for ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./backend ./backend
COPY ./frontend ./frontend

# Expose the port the app runs on
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=backend/app.py

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
