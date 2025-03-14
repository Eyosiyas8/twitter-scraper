# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    jq \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Google's official repository and install the latest Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m scraperuser
USER scraperuser

# Copy requirements first for better caching
COPY --chown=scraperuser:scraperuser requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=scraperuser:scraperuser . .

# Set environment variable for MongoDB
ENV MONGO_URI="mongodb://mongodb:27017/"

# Set entry point to run the scraper
CMD ["python", "Scraper/index_new.py"]