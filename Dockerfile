# Use Python 3.10.13 base image
FROM python:3.10.13-slim

# Set working directory
WORKDIR /app

# Copy bot files to working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
