# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Make port 80 available to the world outside this container
EXPOSE 8989

# Define environment variable
ENV OPENAI_API_KEY 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
ENV OPENAI_MODEL_ENGINE gpt-3.5-turbo

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8989", "src.route:app"]