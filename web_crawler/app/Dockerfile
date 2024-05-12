# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN apt update
RUN apt-get update
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt install -y net-tools
RUN apt install -y mc

# Copy the rest of the application code to the container
COPY . .

# CMD ["python3", "app.py"]