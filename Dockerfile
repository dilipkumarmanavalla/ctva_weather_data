# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /ctva_weather_data

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

ENV FLASK_APP=main.py

# Run Flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]