# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for pyodbc and SQL Server ODBC driver
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    gcc \
    g++ \
    curl \
    gnupg2 \
    lsb-release \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-server.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Copy the current directory contents into the container at /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for serving the app
RUN pip install gunicorn

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
