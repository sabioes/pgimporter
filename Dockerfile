# Start with Python base image
FROM python:3.11-slim

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1
# Environment variables for Flask and Gunicorn
ENV FLASK_APP=pgimporter_app
ENV FLASK_ENV=production

# Set working directory
WORKDIR /pgimporter

# Copy the requirements files and install dependencies
COPY requirements.txt /pgimporter/
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application code into the container
COPY . /pgimporter

# Expose the port that Flask will run on as service
EXPOSE 8080

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "60", "--threads", "3", "--workers", "4", "pgimporter_app:app"]