FROM python:3.10-slim-buster

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    portaudio19-dev \
    python3-all-dev && \
    rm -rf /var/lib/apt/lists/*

# Install awscli via pip
RUN pip install --no-cache-dir awscli

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Install PyAudio
RUN pip install pyaudio

# Define the command to run the application
CMD ["python3", "app4.py"]
