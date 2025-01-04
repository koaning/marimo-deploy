# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Install the required dependencies
RUN python -m venv venv 
RUN venv/bin/python -m pip install -r requirements.txt && venv/bin/python -m spacy download en_core_web_sm

# Command to run the application
CMD ["venv/bin/python", "app.py"]
