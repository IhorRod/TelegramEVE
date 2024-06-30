# Use Python 3.9.8 as the base image
FROM python:3.9.8

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use python-dotenv to load environment variables
RUN pip install "python-dotenv[cli]"

# Run main.py when the container launches
CMD ["python", "-m", "dotenv", "run", "--", "python", "main.py"]