# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Install the required dependencies
RUN python -m pip install uv
RUN python -m uv venv --seed && uv pip install -r requirements.txt && uv run spacy download en_core_web_sm
RUN uv run spacy info 

# Command to run the application
CMD ["uv", "run", "app.py"]
