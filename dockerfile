# Use the official Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt file to the container
COPY requirements.txt /code/

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the container
COPY . /code/

# Run database migrations
RUN python manage.py migrate

# Expose the port used by the Django application
EXPOSE 8010

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]
