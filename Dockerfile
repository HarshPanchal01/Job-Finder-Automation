# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ src/
COPY README.md .

# Create a directory for output files (if needed, though usually mapped via volume)
# But the script writes to current dir, so /app is fine.

# Run the application
CMD ["python", "src/main.py"]
