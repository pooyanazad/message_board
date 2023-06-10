# Set the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app


# Install the required Python packages
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 443

# Set the command to run the application
CMD ["python", "app.py"]
