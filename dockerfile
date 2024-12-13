# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /immfly_task

# Install dependencies
COPY requirements.txt /immfly_task/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /immfly_task/

# Expose the port
EXPOSE 8000

CMD [ "ifconfig" ]
# Run the Django development server
CMD ["python", "/immfly_task/immfly_task/manage.py", "runserver", "0.0.0.0:8000"]
