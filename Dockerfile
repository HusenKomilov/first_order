# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the current directory contents into the container
COPY . /app/

# Step 5: Expose the port the app runs on
EXPOSE 8000

# Step 6: Define the command to run your app using manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
