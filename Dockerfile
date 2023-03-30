# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run Cryptobot.py when the container launches
#CMD ["python", "Cryptobot.py"]
CMD ["uvicorn", "Cryptobot:app", "--host", "0.0.0.0", "--port", "8080"]
